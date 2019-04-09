import pygame

LAT_STEP = 0.002
LON_STEP = 0.008


def keylogger(event, mp, group):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F7 and mp.zoom > 0:
            mp.set(zoom=mp.zoom - 1)
        elif event.key == pygame.K_F9 and mp.zoom < 17:
            mp.set(zoom=mp.zoom + 1)
        elif event.key == pygame.K_UP:
            mp.set(lat=mp.lat + LAT_STEP * 2**(15 - mp.zoom))
        elif event.key == pygame.K_DOWN:
            mp.set(lat=mp.lat - LAT_STEP * 2**(15 - mp.zoom))
        elif event.key == pygame.K_LEFT:
            mp.set(lon=mp.lon - LON_STEP * 2**(15 - mp.zoom))
        elif event.key == pygame.K_RIGHT:
            mp.set(lon=mp.lon + LON_STEP * 2**(15 - mp.zoom))
        elif event.key == pygame.K_F1:
            mp.set(type='map')
        elif event.key == pygame.K_F2:
            mp.set(type='sat')
        elif event.key == pygame.K_F3:
            mp.set(type='sat,skl')
        elif event.key == pygame.K_F4:
            if 'trf' in mp.type:
                mp.set(type=','.join(mp.type.split(',')[:-1]))
            else:
                mp.set(type=mp.type + ',trf')
        else:
            group.key_pressed(event, mp)


def mouselogger(event, mp):
    pass
