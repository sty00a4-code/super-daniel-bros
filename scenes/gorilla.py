from player_module.player import Player, State
from bosses.gorilla import Gorilla, GorillaState
from scenes.scene import Scene

scene = Scene()

def pause(dt: float, game, scene: Scene):
    game.player.state = State.Idle
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.state = GorillaState.Idle
    game.boss.update(dt, game)
    game.boss.animations.update(dt)

def duck_move_in(dt: float, game, scene: Scene):
    game.player.state = State.Walk
    game.boss.state = GorillaState.Walk
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
        game.boss.rect.x = 480 - game.boss.rect.w
        game.boss.rect.y = 270 - (64 + 32)
        
    game.player.move(1)
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.move(-1)
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(duck_move_in, 0.1)

def gorilla_challanges(dt: float, game, scene: Scene):
    game.player.state = State.Idle
    game.boss.state = GorillaState.Challenge
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(gorilla_challanges, 2)

def duck_pos1(dt: float, game, scene: Scene):
    game.player.state = State.Pos1
    game.boss.state = GorillaState.Wait
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(duck_pos1, 1)

def gorilla_pos1(dt: float, game, scene: Scene):
    game.player.state = State.Idle
    game.boss.state = GorillaState.Pos1
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(gorilla_pos1, 1)

def duck_pos1(dt: float, game, scene: Scene):
    game.player.state = State.Pos1
    game.boss.state = GorillaState.Wait
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(duck_pos1, 1)

def gorilla_pos2(dt: float, game, scene: Scene):
    game.player.state = State.Idle
    game.boss.state = GorillaState.Pos2
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(gorilla_pos2, 1)

def duck_pos2(dt: float, game, scene: Scene):
    game.player.state = State.Pos2
    game.boss.state = GorillaState.Wait
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(duck_pos2, 1)

def gorilla_pos3(dt: float, game, scene: Scene):
    game.player.state = State.Idle
    game.boss.state = GorillaState.Pos3
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(gorilla_pos3, 1)

def duck_pos3(dt: float, game, scene: Scene):
    game.player.state = State.Pos3
    game.boss.state = GorillaState.Wait
    
    if scene.timer == 0:
        game.player.animations.play(game.player.state.value)
        game.boss.animations.play(game.boss.state.value)
    
    game.player.update(dt, game)
    game.player.animations.update(dt)
    
    game.boss.update(dt, game)
    game.boss.animations.update(dt)
scene.add(duck_pos3, 1)