from bot import bot
from hikari import Status
import uvloop

if __name__ == "__main__":
    uvloop.install()
    bot.main(Status.DO_NOT_DISTURB)
