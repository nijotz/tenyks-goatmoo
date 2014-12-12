from tenyksservice import TenyksService, run_service, FilterChain
from goattower import db, engine, init
from goattower.models import Actor, User


class GoatMOO(TenyksService):
    irc_message_filters = {
        'goat': FilterChain([r"^(?i)goat ?(?P<cmd>(.*))?$"], private_only=True)
    }

    help_text = 'help'

    def handle_goat(self, data, match):
        nick = data['nick']

        user = db.session.query(User).filter(User.name == nick).first()
        if not user:
            actor = Actor(name=nick)
            actor.parent_id = 1
            db.session.add(actor)
            db.session.commit()
            user = User(name=nick)
            user.actor_id = actor.id
            db.session.add(user)
            db.session.commit()

        cmd = match.groupdict()['cmd']
        if not cmd:
            cmd = 'look'

        self.logger.debug('Goat command: {cmd}'.format(cmd=cmd))
        engine.handle_text(user.actor.id, cmd)

        for text in engine.get_text(user.actor.id):
            for line in text.split('\n'):
                if line == '':
                    line = ' '
                self.send(line, data)


def main():
    init()
    run_service(GoatMOO)


if __name__ == '__main__':
    main()
