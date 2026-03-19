"""
Lightweight HTTP server to keep Render free-tier web service alive.
UptimeRobot (or any monitor) pings the /health endpoint every 5 minutes
to prevent the service from sleeping.
"""

from aiohttp import web
import asyncio
import os

PORT = int(os.getenv('PORT', 8080))

async def health_check(request):
    return web.json_response({
        'status': 'alive',
        'service': 'discord-order-bot'
    })

async def home(request):
    return web.Response(
        text='🤖 Discord Order Bot is running!',
        content_type='text/plain'
    )

async def start_server():
    app = web.Application()
    app.router.add_get('/', home)
    app.router.add_get('/health', health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f'  🌐  Keep-alive server running on port {PORT}')
    return runner
