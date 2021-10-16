import asyncio

from git import Repo
from git.exc import GitCommandError

from gaganrobot import gaganrobot, Message, Config

LOG = gaganrobot.getLogger(__name__)
CHANNEL = gaganrobot.getCLogger(__name__)


@gaganrobot.on_cmd("update", about={
    'header': "Check Updates or Update GaganRobot",
    'flags': {
        '-pull': "pull updates",
        '-master': "select master branch",
        '-beta': "select beta branch"},
    'usage': "{tr}update : check updates from master branch\n"
             "{tr}update -[branch_name] : check updates from any branch\n"
             "add -pull if you want to pull updates",
    'examples': "{tr}update -beta -pull"}, del_pre=True, allow_channels=False)
async def check_update(message: Message):
    """ check or do updates """
    await message.edit("`Checking for updates, please wait....`")
    flags = list(message.flags)
    pull_from_repo = False
    branch = "master"
    if "pull" in flags:
        pull_from_repo = True
        flags.remove("pull")
    if len(flags) == 1:
        branch = flags[0]
        dev_branch = "alpha"
        if branch == dev_branch:
            await message.err('Can\'t update to unstable [alpha] branch. '
                              'Please use other branches instead !')
            return
    repo = Repo()
    if branch not in repo.branches:
        await message.err(f'invalid branch name : {branch}')
        return
    try:
        out = _get_updates(repo, branch)
    except GitCommandError as g_e:
        await message.err(g_e, del_in=5)
        return
    if pull_from_repo:
        if out:
            await message.edit(f'`New update found for [{branch}], Now pulling...`')
            await _pull_from_repo(repo, branch)
            await CHANNEL.log(f"**PULLED update from [{branch}]:\n\n📄 CHANGELOG 📄**\n\n{out}")
            await message.edit('**GaganRobot Successfully Updated!**\n'
                               '`Now restarting... Wait for a while!`', del_in=3)
            asyncio.get_event_loop().create_task(gaganrobot.restart(True))
        else:
            active = repo.active_branch.name
            if active == branch:
                await message.err(f"already in [{branch}]!")
                return
            await message.edit(
                f'`Moving HEAD from [{active}] >>> [{branch}] ...`', parse_mode='md')
            await _pull_from_repo(repo, branch)
            await CHANNEL.log(f"`Moved HEAD from [{active}] >>> [{branch}] !`")
            await message.edit('`Now restarting... Wait for a while!`', del_in=3)
            asyncio.get_event_loop().create_task(gaganrobot.restart())
    else:
        if out:
            change_log = f'**New UPDATE available for [{branch}]:\n\n📄 CHANGELOG 📄**\n\n'
            await message.edit_or_send_as_file(change_log + out, disable_web_page_preview=True)
        else:
            await message.edit(f'**GaganRobot is up-to-date with [{branch}]**', del_in=5)


def _get_updates(repo: Repo, branch: str) -> str:
    repo.remote(Config.UPSTREAM_REMOTE).fetch(branch)
    out = ''
    upst = Config.UPSTREAM_REPO.rstrip('/')
    for i in repo.iter_commits(f'HEAD..{Config.UPSTREAM_REMOTE}/{branch}'):
        out += f"🔨 **#{i.count()}** : [{i.summary}]({upst}/commit/{i}) 👷 __{i.author}__\n\n"
    return out


async def _pull_from_repo(repo: Repo, branch: str) -> None:
    repo.git.checkout(branch, force=True)
    repo.git.reset('--hard', branch)
    repo.remote(Config.UPSTREAM_REMOTE).pull(branch, force=True)
    await asyncio.sleep(1)
