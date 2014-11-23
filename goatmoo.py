from tenyksservice import TenyksService, run_service, FilterChain
from goattower.engine import handle_text, get_text, session
from goattower.models import Actor, User


class GoatMOO(TenyksService):
    irc_message_filters = {
        'goat': FilterChain([r"^(?i)goat ?(?P<cmd>(.*))?$"], private_only=True)
    }

    help_text = 'help'

    def handle_goat(self, data, match):
        nick = data['nick']

        user = session.query(User).filter(User.name == nick).first()
        if not user:
            actor = Actor(name=nick)
            actor.parent_id = 1
            session.add(actor)
            session.commit()
            user = User(name=nick)
            user.actor_id = actor.id
            session.add(user)
            session.commit()

        cmd = match.groupdict()['cmd']
        if not cmd:
            cmd = 'look'

        self.logger.debug('Goat command: {cmd}'.format(cmd=cmd))
        handle_text(user.actor.id, cmd)

        for line in get_text(user.actor.id):
            self.send(line.replace('\n', ''), data)


def main():
    run_service(GoatMOO)


if __name__ == '__main__':
    main()
