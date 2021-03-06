"""Heroes view"""
from flask_restful import Resource

from models.hero import Hero
from modules.hero import HeroModule
from flask import request


class HeroesHandler(Resource):
    """Heroes handler"""

    def get(self):
        """Get heroes"""
        try:
            # Fazendo a consulta no banco de dados
            heroes = Hero.get_heroes(request.args.get('cursor'))

            # Montando a resposta, por enquanto iremos deixar o cursor vazio
            response = {
                'cursor': None,
                'heroes': []
            }
            # Vamos percorer os herois e transformar em json
            for hero in heroes:
                response['heroes'].append(hero.to_dict())

                # Adicionando o cursor na resposta
            if len(response['heroes']) == 16:
                response['cursor'] = response['heroes'][-1]['id']

            return response

        except Exception as error:
            return {
                       'message': 'Error on get heroes',
                       'details': str(error)
                   }, 500

    def post(self):
        """Create a new hero"""
        try:

            hero = HeroModule.create(request.json['hero'])
            return hero.to_dict()

        except Exception as error:
            return {
                       'message': 'Error on create a new hero',
                       'details': str(error)
                   }, 500


class HeroHandler(Resource):
    """Hero handler"""

    def get(self, hero_id):
        """Get hero"""
        try:

            heroes = Hero.get_hero(hero_id)
            if not heroes:
                return {'message': 'Hero not found'}, 404
            return heroes.to_dict()

        except Exception as error:
            return {
                       'message': 'Error on get hero',
                       'details': str(error)
                   }, 500

    def post(self, hero_id):
        """Update a hero"""
        try:

            hero = Hero.get_hero(hero_id)
            if not hero or 'hero' not in request.json:
                return {'message': 'Bad request'}, 404
            HeroModule.update(hero, request.json['hero'])
            return hero.to_dict()

        except Exception as error:
            return {
                       'message': 'Error on update hero',
                       'details': str(error)
                   }, 500

    def delete(self, hero_id):
        """Delete hero"""
        try:
            hero = Hero.delete(hero_id)
            return {'message': 'Hero deleted'}

        except Exception as error:
            return {
                       'message': 'Error on delete hero',
                       'details': str(error)
                   }, 500
