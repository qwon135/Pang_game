# 파이게임 만들기 기본 뼈대
import pygame
import os
#######################################################

pygame.init() 
# 기본 초기화(반드시필요)

screen_width=640
screen_height=480
# 가로,세로크기
screen=pygame.display.set_mode((screen_width,screen_height))

# 화면타이틀설정
pygame.display.set_caption("Nado Pang")
# 게임이름

#FPS
clock=pygame.time.Clock()
######################################################

# 1. 사용자 게임 초기화(배경화면, 게임이미지, 좌표, 폰트 등)
current_path=os.path.dirname(__file__)#현재 파일의 위치를 반환 해주는 모듈
image_path=os.path.join(current_path,"images")

#배경만들기
background=pygame.image.load(os.path.join(image_path,"background.bmp"))

#스테이지 만들기
stage=pygame.image.load(os.path.join(image_path,"stage.bmp"))
stage_size=stage.get_rect().size
stage_height=stage_size[1] #스테이지 높이 위에 캐릭터를 두기위해 값을 생성

#캐릭터 만들기
character=pygame.image.load(os.path.join(image_path,"character.bmp"))
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=(screen_width/2)-(character_width/2)
character_y_pos=screen_height-character_height-stage_height

#캐릭터 이동 방향
character_to_x=0

#캐릭터 이동 속도
character_speed=5

#무기만들기
weapon=pygame.image.load(os.path.join(image_path,"weapon.bmp"))
weapon_size=weapon.get_rect().size
weapon_width=weapon_size[0]

#무기는 한번에 여러발 발사 가능
weapons=[]

#무기 이동 속도
weapon_speed=10



running=True
while running:
    dt=clock.tick(60)#게임 화면 초당 프레임 수
    # print("fps:"+str(clock.get_fps()))
# 2. 이벤트 처리

    for event in pygame.event.get(): 
    # 파이게임 시장을 위해 무 조건 있어야함(사용자가 마우스,키보드를 클릭하는지감시)
        if event.type==pygame.QUIT:
            # 창이닫히는 이벤트가 발생하였는가?
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                character_to_x-=character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x+=character_speed
            elif event.key==pygame.K_SPACE:#무기발사
                weapon_x_pos=character_x_pos-character_width/2-weapon_width/2
                weapon_y_pos=character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])
        if event.type==pygame.KEYUP:
            if event.key== pygame.K_LEFT or event.key==pygame.K_RIGHT:
                character_to_x=0       
    
    
    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos> screen_width-character_width:
        character_x_pos=screen_width=character_width
    
    #무기 위치 조정
    # (100,200)무기위치 -> 위로 쏘니까 올라감 Y좌표는 줄어듬 195,185,180....
    # (500,200)무기위치 -> 위로 쏘니까 올라감 Y좌표는 줄어듬 195,185,180.... 
    # 그래서 weapon_speed를 빼줘서 y 값을초기화 시킴
    weapons=[[w[0],w[1]-weapon_speed] for w in weapons] #무기 위치를 위로 올림

    #천장에 닿은 무기 없애기
    weapons=[ [w[0],w[1]] for w in weapons if w[1] >0]
    # 4. 충돌 처리
        
    # 5 화면에 그리기
    screen.blit(background,(0,0))
    
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
    
    screen.blit(stage,(0,(screen_height-stage_height)))
    screen.blit(character,(character_x_pos,character_y_pos))
    
    

    pygame.display.update()
    # 게임 화면 다시 그리기 


pygame.quit()