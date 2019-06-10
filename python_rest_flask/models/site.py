from sql_alchemy import banco

class SiteModel(banco.Model):

    __tablename__ = 'sites'

    #mapeia para o sqlalchemy que essa classe é uma tabela no banco de dados
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel') # lista de objetos hoteis

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'site_id': self.site_id,
            'site': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        #select * from sites where url = url
        #first() seleciona o primeiro 
        site = cls.query.filter_by(url = url).first() #cls é a abreviação da classe

        if site: # if hotel is not None
            return site
        return None
        # consulta no banco
   
    @classmethod
    def find_by_id(cls, site_id):
        #select * from sites where url = url
        #first() seleciona o primeiro 
        site = cls.query.filter_by(site_id = site_id).first() #cls é a abreviação da classe

        if site: # if hotel is not None
            return site
        return None
        # consulta no banco

    def save_site(self):
        #abre conexao com o banco
        #salva o proprio objeto no banco
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        #deletando todos os hoteis associados ao site
        [hotel.delete_hotel() for hotel in self.hoteis]
        #deleta o site
        banco.session.delete(self)
        banco.session.commit()