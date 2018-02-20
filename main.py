import pyglet

pyglet.resource.path = ['assets']
window = pyglet.window.Window()
image = pyglet.resource.image('Player1.png')

@window.event
def on_draw():
    window.clear()
    image.blit(0,0)

pyglet.app.run()
