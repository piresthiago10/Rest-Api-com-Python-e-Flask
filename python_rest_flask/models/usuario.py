from sql_alchemy import banco

class UserModel(banco.Model):

    __tablename__ = 'usuarios'

    #mapeia para o sqlalchemy que essa classe é uma tabela no banco de dados
    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    #não passando o user_id, o SQLAlchemy vai identificá-lo como autoincrement pois ele é um primary key
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def jsnon(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first() #cls é a abreviação da classe

        if user: # if user is not None
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login = login).first() #cls é a abreviação da classe

        if user: # if user is not None
            return user
        return None    
   
    def save_user(self):
        #abre conexao com o banco
        #salva o proprio objeto no banco
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()