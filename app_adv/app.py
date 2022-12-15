from aiohttp import web
from views import OwnerView, AdvertisementView
from models import Base
from database import engine
from middlewares import session_middleware

app = web.Application()


async def orm_context(app:web.Application):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose() 
    print('SHOUTDOWN')


app.cleanup_ctx.append(orm_context)

app.add_routes(
    [
        web.get('/owners/{owner_id:\d+}', OwnerView),
        web.patch('/owners/{owner_id:\d+}', OwnerView),
        web.delete('/owners/{owner_id:\d+}', OwnerView),
        web.post('/owners/', OwnerView),
        web.get('/ads/{advertisement_id:\d+}', AdvertisementView),
        web.patch('/ads/{advertisement_id:\d+}', AdvertisementView),
        web.delete('/ads/{advertisement_id:\d+}', AdvertisementView),
        web.post('/ads/', AdvertisementView)
    ]
)
app.middlewares.append(session_middleware)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
