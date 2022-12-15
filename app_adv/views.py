import json
from aiohttp import web
from database import Session
from models import OwnerModel, AdvertisementModel


async def get_owner(owner_id: int, session: Session):
    owner = await session.get(OwnerModel, owner_id)
    if owner is None:
        raise web.HTTPNotFound(text=json.dumps(
            {
                'status': 'error',
                'description': 'owner not found'
            }
        ), content_type='application/json')
    return owner


def owner_to_dict(owner: OwnerModel):

    return ({
        'id': owner.id,
        'email': owner.email
    })


async def get_advertisement(advertisement_id: int, session: Session):
    advertisement = await session.get(AdvertisementModel, advertisement_id)
    if advertisement is None:
        raise web.HTTPNotFound(text=json.dumps(
            {
                'status': 'error',
                'description': 'advertisement not found'
            }
        ), content_type='application/json')
    return advertisement


def advertisement_to_dict(advertisement: AdvertisementModel):

    return ({'id': advertisement.id,
            'title': advertisement.title,
            'description': advertisement.description,
            'created_at' : str(advertisement.created_at),
            'owner_id': advertisement.owner_id
            })


class OwnerView(web.View):

    @property
    def session(self):
        return self.request['session']


    async def get(self):
        owner_id = int(self.request.match_info['owner_id'])
        owner = await get_owner(owner_id, self.session)
        return web.json_response(
            owner_to_dict(owner)
        )


    async def post(self):
        owner_data = await self.request.json()
        new_owner = OwnerModel(**owner_data)
        self.session.add(new_owner)
        await self.session.commit()
        return web.json_response(
            owner_to_dict(new_owner)
        )


    async def patch(self):
        owner_id = int(self.request.match_info['owner_id'])
        owner_patch = await self.request.json()
        owner = await get_owner(owner_id, self.session)
        for field, value in owner_patch.items():
            setattr(owner, field, value)
        self.session.add(owner)
        await self.session.commit()
        return web.json_response(
            owner_to_dict(owner)
        )


    async def delete(self):
        owner_id = int(self.request.match_info['owner_id'])
        owner = await get_owner(owner_id, self.session)
        await self.session.delete(owner)
        await self.session.commit()
        return web.json_response({'status': 'deleted'})


class AdvertisementView(web.View):

    @property
    def session(self):
        return self.request['session']


    async def get(self):
        advertisement_id = int(self.request.match_info['advertisement_id'])
        advertisement = await get_advertisement(advertisement_id, self.session)
        return web.json_response(advertisement_to_dict(advertisement))


    async def post(self):
        advertisement_data = await self.request.json()
        new_advertisement = AdvertisementModel(**advertisement_data)
        self.session.add(new_advertisement)
        await self.session.commit()
        return web.json_response(advertisement_to_dict(new_advertisement))


    async def patch(self):
        advertisement_id = int(self.request.match_info['advertisement_id'])
        advertisement_data = await self.request.json()
        advertisement = await get_advertisement(advertisement_id, self.session)
        for field, value in advertisement_data.items():
            setattr(advertisement, field, value)
        self.session.add(advertisement)
        await self.session.commit()
        return web.json_response(advertisement_to_dict(advertisement))


    async def delete(self):
        advertisement_id = int(self.request.match_info['advertisement_id'])
        advertisement = await get_advertisement(advertisement_id, self.session)
        await self.session.delete(advertisement)
        await self.session.commit()
        return web.json_response({'status': 'deleted'})
