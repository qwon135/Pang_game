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

# 공 만들기(4개 크기에 대해 따로 처리)
ball_images=[
    pygame.image.load(os.path.join(image_path,"balloon1.bmp")),
    pygame.image.load(os.path.join(image_path,"balloon2.bmp")),
    pygame.image.load(os.path.join(image_path,"balloon3.bmp")),
    pygame.image.load(os.path.join(image_path,"balloon4.bmp"))
    ]

# 공 크기에 따른 최초 스피트(클수록 빠름)
ball_speed_y=[-18,-15,-12,-9] # index 0,1,2,3에 해당하는 값

#공들
balls=[]

#공마다 특징이 많아 딕셔너리 사용
#최초로 발생하는 큰공 추가
balls.append({
    "pos_x":50, #공의 x 좌표
    "pos_y":50, #공의 y 좌표
    "img_idx":0, #어떤 공 이미지를 쓸지(인덱스)
    "to_x":3, #공의 x축 이동방향, -3이면 왼쪽 3이면 오른쪽
    "to_y":-6, #y축 이동 방향
    "init_spd_y":ball_speed_y[0]#y의 최초 속도를 정의
})

#사라질 무기, 공 정보 저장 변수
weapon_to_remove=-1
ball_to_remove=-1


running=True
while running:
    dt=clock.tick(50)#게임 화면 초당 프레임 수
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
        character_x_pos=screen_width-character_width
    
    #무기 위치 조정
    # (100,200)무기위치 -> 위로 쏘니까 올라감 Y좌표는 줄어듬 195,185,180....
    # (500,200)무기위치 -> 위로 쏘니까 올라감 Y좌표는 줄어듬 195,185,180.... 
    # 그래서 weapon_speed를 빼줘서 y 값을초기화 시킴
    weapons=[[w[0],w[1]-weapon_speed] for w in weapons] #무기 위치를 위로 올림

    #천장에 닿은 무기 없애기
    weapons=[ [w[0],w[1]] for w in weapons if w[1] >-250]
    
    #공의 위치 정의
    for ball_idx,ball_val in enumerate(balls): #
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]

        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width=ball_size[0]
        ball_height=ball_size[1]

        #볼이 가로 벽에 닿으면 튕겨져 나와서 반대방향으로 바꿔줌
        if ball_pos_x<=0 or ball_pos_x>screen_width-ball_width:
             ball_val["to_x"]=ball_val["to_x"]*-1
        #세로위치
        #스테이지에 튕겨서 올라가는 공 처리
        if ball_pos_y >= screen_height-stage_height-ball_height:
            ball_val["to_y"] =ball_val["init_spd_y"]
        else: #그외의 모든 경우에는 속도 증가
            ball_val["to_y"]+=0.5
        
        ball_val["pos_x"]+=ball_val["to_x"]
        ball_val["pos_y"]+=ball_val["to_y"]
    # 4. 충돌 처리

    #캐릭터 rect 정보 업데이트
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos
        
    for ball_idx,ball_val in enumerate(balls): 
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]

        #공 rect 정보 업데이트
        ball_rect=ball_images[ball_img_idx].get_rect()
        ball_rect.left=ball_pos_x
        ball_rect.top=ball_pos_y
        
        #공과 캐릭 충돌 체크
        if character_rect.colliderect(ball_rect):
            running=False
            break
        
        #공과 무기 충돌 처리(무기는 여러개 이므로 for,list사용)
        for weapon_idx,weapon_val in enumerate(weapons):
            weapon_x_pos=weapon_val[0]
            weapon_y_pos=weapon_val[1]

            #무기 rect정보 업데이트
            weapon_rect=weapon.get_rect()
            weapon_rect.left=weapon_x_pos
            weapon_rect.top=weapon_y_pos

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove=weapon_idx #해당 무기 없애기 위한 값 설정
                ball_to_remove=ball_idx #해당 공 없애기 위한 값 설정
                break
    #충돌된 공 or 무기 없애기
    if ball_to_remove >-1:
        del balls[ball_to_remove]
        ball_to_remove=-1
    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1

    # 5 화면에 그리기
    screen.blit(background,(0,0))
    
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
    
    for idx,val in enumerate(balls):
        ball_pos_x=val["pos_x"]
        ball_pos_y=val["pos_y"]
        ball_img_idx=val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_pos_x,ball_pos_y))

    screen.blit(stage,(0,(screen_height-stage_height)))
    screen.blit(character,(character_x_pos,character_y_pos))
    
    

    pygame.display.update()
    # 게임 화면 다시 그리기 


pygame.quit()