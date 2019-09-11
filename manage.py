from app import manager, db


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)

    def __str__(self):
        return self.name.upper()

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other


if __name__ == '__main__':
    manager.run()