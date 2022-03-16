#狼人殺
import random
import _staticdata
roadname = _staticdata.pd_roadname()

#建立遊戲
def create(redis_model, group_id):
    redis_model.game_room = redis_model.reply('game_wolf')
    if group_id in redis_model.game_room.keys() : return False
    room = 'w'
    for i in range(0,6):           
        room += str(random.randint(0,9))
    while room in redis_model.game_room.values():
        room += str(random.randint(0,9))
    redis_model.game_room[group_id] = room
    data = {
        'game_list' : {},
        'game_turn' : {'0' : False}
        }
    redis_model.insert('game_wolf', redis_model.game_room)
    redis_model.insert(room, data)
    return room

#操作介面
class flex_simulator():
    def __init__(self):
        self.image = {
            'start' : 'https://i.imgur.com/b0CJ5JV.png?1',
            'daylight' : 'https://i.imgur.com/MzrEAlu.jpg',
            'night' : 'https://i.zgjm.org/img/new/98460.jpg',
            'vote' : 'https://i.imgur.com/OYzTsaz.jpg?1'
            }
        self.text = {
            'daylight' : None,
            'night' : '天黑請閉眼， 狼人出沒中'            
            }
        self.flex_carousel = {'contents':[],'type':'carousel'}
        self.separator = {'type': 'separator', 'color' : '#7A7A7A'}
    def base_box(self, layout):
        box = {
            'type': 'box',
            'layout': layout,
            'contents': []
                }
        return box
    def image_box(self, image):
        box = {
            'type': 'image',
            'url': image,
            'size': 'full',
            'aspectMode': 'cover'
                }
        return box
    def text_box(self, text, color):
        box = {
            'type': 'text',
            'text': text,
            'weight': 'bold',
            'color': color,
            'wrap' : True,
            'size': 'sm'
                }
        return box
    def button_box(self, backgroundColor):
        box = {
            'type': 'box',
            'layout': 'horizontal',
            'backgroundColor': backgroundColor,
            'contents': []
            } 
        return box
    def button(self,color, label, data):
        box = {
            'type': 'button',
            'color' : color,
            'style' : 'primary'
            }
        box['action'] = {
            'type': 'postback',
            'label': label,
            'data': data
                }
        return box
    def rowbox(self, color):
        box = {
            'type': 'box',
            'layout': 'horizontal',
            'backgroundColor': color,
            'height': '24px',
            'contents': []
        }
        return box
    def spacebox(self, text, color):
        box = {
            'type': 'text',
            'text': text,
            'align': 'center',
            'color': color,
            'size': 'sm',
            'wrap': True,
            'adjustMode': 'shrink-to-fit'
        }
        return box
    def postbackbox(self, label, data):
        box = {
            'type' : 'postback',
            'label' : label,
            'data' : data
        }
        return box
    def start(self, room):
        game = {
            'type': 'bubble',
            'size' : 'giga',
            }
        game['header'] = self.base_box(layout = 'vertical')
        game['header']['paddingAll'] = 'None'
        game['header']['backgroundColor'] = '#1C1C1C'
        text = self.text_box(text= '遊戲說明 : 遊戲開始之後私訊炎炎輸入: {room}-我是誰 \n炎炎會跟你說你的身分!\n目前只有狼人，其他村民無功能'.format(room = room), color= '#EDEDED')
        text['size'] = 'xl'
        text['align'] = 'center'
        text['offsetStart'] = 'md'
        game['header']['contents'].append(text)
        game['hero'] = self.image_box(image= self.image['start'])
        game['hero']['aspectRatio'] = '13:9'        
        game['footer'] = self.base_box('vertical')
        game['footer']['backgroundColor'] = '#D1D1D1'
        buttonbox = self.button_box(backgroundColor= '#D1D1D1')
        buttonbox['contents'].append(self.button(color= '#4D000F', label= '參加', data= '狼人殺0-參加-'+ room))
        buttonbox['contents'].append(self.button(color= '#4D000F', label= '取消', data= '狼人殺0-取消-'+ room))
        buttonbox['contents'].append(self.button(color= '#4D000F', label= '開始'.format(room = room), data= '狼人殺1-開始-'+ room))
        game['footer']['contents'].append(buttonbox)
        return game
    def vote(self, turn, time,  alive):
        game = {
            'type': 'bubble',
            'size' : 'giga',
            }
        game['header'] = self.base_box(layout = 'vertical')
        game['header']['backgroundColor'] = '#1A1A1A'
        text = self.text_box(text= self.text[time], color= '#EDEDED')
        text['size'] = 'xxl'
        game['header']['contents'].append(text)
        game['hero'] = self.image_box(image= self.image[time])        
        game['hero']['aspectRatio'] = '13:9'
        base = self.base_box(layout= 'vertical')
        base['paddingAll'] = 'None'
        base['spacing'] = 'xs'
        game['body'] = base
        row = self.rowbox(color = '#3C3C3C')
        for i in random.choices(roadname['name'], k = 2):
            space = self.spacebox(text= i, color= '#FFFFFF')
            row['contents'].append(space)
        game['body']['contents'].append(row)
        for i in range(len(alive)):
            if i % 2 != 0 and i != 0 : continue
            row = self.rowbox(color = '#C2C2C2')
            for j in range(2):
                space = self.spacebox(text= list(alive.values())[i], color= '#000000')
                space['action'] = self.postbackbox(
                    label = '投票', 
                    data = '狼人殺-投票-{turn}-{UID}'.format(turn = turn, UID = list(alive.keys())[i])
                    )
                row['contents'].append(space)
                i += 1                
                if i >= len(alive) : break
            game['body']['contents'].append(row)
        self.flex_carousel['contents'].append(game)
        return
    def check(self, redis_model ,room, round):
        data = redis_model.reply(room)
        alive = data['alive']
        menu = data['menu']
        count_max = sum(menu.values())
        game = {
            'type': 'bubble',
            'size' : 'mega',
            }
        game['header'] = self.base_box(layout = 'vertical')
        game['header']['paddingAll'] = 'None'
        game['header']['backgroundColor'] = '#2F4F00'
        text = self.text_box(text= '投票結果確認', color= '#EDEDED')
        text['size'] = 'xl'
        text['align'] = 'center'
        text['offsetStart'] = 'md'
        game['header']['contents'].append(text)
        game['hero'] = self.base_box(layout = 'vertical')
        game['hero']['paddingAll'] = 'None'
        game['hero']['backgroundColor'] = '#FFFFFF'
        text = self.text_box(text= '重新整理', color= '#171717')
        text['align'] = 'start'
        text['action'] = self.postbackbox(
            label = '重新整理', 
            data = '狼人殺-投票重整-{turn}-'.format(turn = round)
            )
        game['hero']['contents'].append(text)
        base = self.base_box(layout= 'vertical')
        base['paddingAll'] = 'None'
        game['body'] = base
        row = self.rowbox(color = '#548C00')
        for i in ['村民', '票數']:
            space = self.spacebox(text= i, color= '#FFFFFF')
            space['size'] = 'md'
            row['contents'].append(space)
        game['body']['contents'].append(row)
        for i in range(len(menu)):
            UID = list(alive.keys())[i]
            row = self.rowbox(color = '#EDEDED')            
            space = self.spacebox(text= list(alive.values())[i], color= '#000000')
            space['action'] = self.postbackbox(
                label = '投票', 
                data = '狼人殺-投票改-{turn}-{UID}'.format(turn = round, UID = UID)
                )
            row['contents'].append(space)
            box = self.base_box(layout = 'vertical')
            baseline = self.base_box(layout = 'baseline')
            baseline['width'] = str(int(int(menu[UID]) / count_max * 100)) + '%'
            baseline['backgroundColor'] = '#FF6666'
            baseline['height'] = '24px'
            box['contents'].append(baseline)
            row['contents'].append(box)
            game['body']['contents'].append(row)
            game['body']['contents'].append(self.separator)
        game['footer'] = self.base_box(layout = 'vertical')
        game['footer']['paddingAll'] = 'None'
        game['footer']['backgroundColor'] = '#2F4F00'
        text = self.text_box(text= '確認洗洗睡', color= '#D1D1D1')
        text['size'] = 'xl'
        text['align'] = 'center'
        game['footer']['contents'].append(text)
        game['footer']['action'] = self.postbackbox(
            label = '投票確認', 
            data = '狼人殺-投票確認-{turn}-{UID}'.format(turn = round, UID = UID)
            )
        self.flex_carousel['contents'].append(game)
        return
    def sleep(self, round, dead):
        game = {
            'type': 'bubble',
            'size' : 'mega',
            }        
        game['header'] = self.base_box(layout = 'vertical')
        game['header']['paddingAll'] = 'None'
        game['header']['backgroundColor'] = '#4D0000'
        text = self.text_box(text= '投票處決玩家 : \n'+ '\n'.join(dead), color= '#D1D1D1')
        text['size'] = 'xl'
        text['align'] = 'center'
        text['offsetStart'] = 'md'
        game['header']['contents'].append(text)
        game['hero'] = self.image_box(image= self.image['vote'])        
        game['hero']['aspectRatio'] = '13:9'
        game['footer'] = self.base_box(layout = 'vertical')
        game['footer']['paddingAll'] = 'None'
        game['footer']['backgroundColor'] = '#4D0000'        
        text = self.text_box(text= '確認結果', color= '#D1D1D1')
        text['size'] = 'xl'
        text['align'] = 'center'
        game['footer']['contents'].append(text)
        game['footer']['action'] = self.postbackbox(
            label = '投票確認', 
            data = '投票結果-{turn}-'.format(turn = round)
            )
        self.flex_carousel['contents'].append(game)
        return
    def seer(self):
        return

    def winner(self):
        return

#參加遊戲/角色分配
class menu(): 
    def __init__(self, redis_model, data, event, message_action):
        self.ordr, self.room = data.split('-')[1:3]
        self.redis_model = redis_model
        self.data = redis_model.reply(self.room)
        if self.data['game_turn']['0'] == True : 
            message_action.TextMsg(event, '狼人出沒中，遊戲進行中不可以修改遊戲名單~') 
            self.ordr = '跳出'
            return
    def join(self, redis_model, profile_user, event, message_action):
        self.data['game_list'][event.source.user_id] = profile_user
        redis_model.insert(self.room, self.data)
        message_action.TextMsg(event, profile_user +'----加入遊戲成功')
        return
    def cancel(self, redis_model, profile_user, event, message_action):
        del self.data['game_list'][event.source.user_id]
        redis_model.insert(self.room, self.data)
        message_action.TextMsg(event, profile_user +'----取消遊戲成功')
        return

class role(): 
    def __init__(self, redis_model, data, event, message_action):
        self.ordr, self.room = data.split('-')[1:3]
        self.redis_model = redis_model
        self.event = event
        self.message_action = message_action
        self.data = self.redis_model.reply(self.room)
        self.flex_simulator = flex_simulator()
 
    def distribute(self):
        uid = random.choice(list(self.data['game_list'].keys()))
        del self.data['game_list'][uid]
        return uid

    def start(self):
        if len(self.data['game_list']) < 6: 
            self.message_action.TextMsg(self.event, '人數小於6人無法開始遊戲')
            return 
        game = {
            'dead' : [],
            'vote' : {},
            'check' : [],
            'werewolves' : {
                'wolf' : [],
                'minion' : []
                },
            'village' : {
                'seer' : [],
                'witch' : [],
                'hunter' : [],
                'acient' : [],
                'svior' : [],
                'villagers' : []       
                },
            'protect' : [],
            'night' : True,
            'game_turn' : {'0' : True, '1' : False},
            'game_end' : False
        }
        game['alive'] = self.data['game_list'].copy()
        all = len(self.data['game_list'])
        for i in range(2):
            game['werewolves']['wolf'].append(self.distribute())
        game['village']['seer'].append(self.distribute())
        game['village']['hunter'].append(self.distribute())
        for i in range(int((all - 6) / 3)): 
            game['werewolves'][random.choice(['wolf', 'minion'])].append(self.distribute())
            game['village'][random.choice(['seer', 'hunter', 'witch', 'acient', 'svior'])].append(self.distribute())
        for i in list(self.data['game_list'].keys()):
            game['village']['villagers'].append(self.distribute())
        # for i in game['village']['seer']:
        #     game[i] = {'see' : 0, 'turn' : 1}
        # for i in game['village']['witch']:
        #     game[i] = {'poison' : True, 'antidote' : True}
        # for i in game['village']['hunter']:
        #     game[i] = {'deathrattle' : False}
        # for i in game['village']['acient']:
        #     game[i] = {'life' : 2}
        game['werewolves']['all'] = game['werewolves']['wolf']  + game['werewolves']['minion'] 
        game['village']['all'] = game['village']['seer'] + game['village']['hunter'] + game['village']['witch'] + game['village']['acient'] + game['village']['svior'] + game['village']['villagers']
        for i in game['werewolves']['wolf']:
            game[i] = '狼人(現在你不知道夥伴有誰，殺人會從狼人們選擇的人物裡隨機抽選對象)'
        for i in game['werewolves']['minion']:
            game[i] = '狼人爪牙(跟狼人同一隊，目前無功能)'
        for i in game['village']['all']:
            game[i] = '村民(待宰羔羊們)'
        self.data = game
        self.save()
        self.flex_simulator.vote(1, 'night', game['alive'])
        self.message_action.FlexMsg(self.event, '開始遊戲',  self.flex_simulator.flex_carousel)
        return 

    #預言
    def seer(self, uid):
        if self.data[uid]['see'] < self.data[uid]['turn']:
            return True
        else :
            return False

    def save(self):
        self.redis_model.insert(self.room, self.data)


#按鍵
class action():
    def __init__(self, redis_model, room, event, message_action):
        self.redis_model = redis_model
        self.data = redis_model.reply(room)
        self.event = event
        self.message_action = message_action
        self.room = room
        self.round = list(self.data['game_turn'].keys())[-1]
        
#死亡
    def dead(self, kill):
        self.data['dead'].append(kill)
        del self.data['alive'][kill]
        if kill in self.data['werewolves']['all']:
            self.data['werewolves']['all'].remove(kill)
        self.winner()
        return
#狼人
    def wolf(self, play, kill):
        self.data['vote'][play] = kill
        if len(self.data['vote']) == len(self.data['werewolves']['wolf']) :
            kill = random.choice(list(self.data['vote'].values()))
            self.dead(kill)
            self.data['night'] = False
            self.data['game_turn'][self.round] =True
            self.data['game_turn'][int(self.round) +1] = False
            self.data['vote'] = {}
            self.save()
            return True
        self.save()
        return False

# #獵人
#         if uid in self.data['village']['hunter'] :
#             if self.data[uid]['deathrattle']:
#                 self.data['alive'].remove(data)
#                 self.data['dead'].append(data)
#                 self.save()

#投票階段
    def vote(self, play, kill):
        if play in self.data['check']:
            return False
        self.data['vote'][play] = kill
        count_vote = len(self.data['vote'].keys())
        count_alive = len(self.data['alive'])
        if count_vote == count_alive:
            self.data['menu'] = {i: list(self.data['vote'].values()).count(i) for i in self.data['vote'].values()}
            self.save()
            return True
        self.save()
        return None

#確認階段
    def check(self, uid):
        self.data['check'].append(uid)
        count_check = len(self.data['check'])
        count_vote = len(self.data['vote'][uid].keys())
        count_alive = len(self.data['alive'])
        vote_max = max(self.data['menu'].values())
        if count_check == count_alive == count_vote != 1:
            vote = []
            for i in self.data['vote'].keys():
                if self.data['vote'][i] == vote_max:
                    self.dead(self, i)
                    vote.append(i)
            self.data['night'] = True
            self.data['vote'] = {}
            self.data['check'] = []
            self.save()   
            return vote
        self.save()    
        return True
#勝利
    def winner(self):
        if len(self.data['werewolves']['all']) > len(self.data['alive']) /2 -1 :
            text = ', '.join(self.data['werewolves']['all'])
            self.data['game_end'] = True
            self.save()
            self.message_action.TextMsg(self.event, '狼人組織 {text} 獲勝!!!'.format(text = text))
            return 'winner'
        elif len(self.data['werewolves']['wolf']) == 0 :
            text = ', '.join(self.data['village']['all'])
            self.data['game_end'] = True
            self.save()
            self.message_action.TextMsg(self.event, '小鎮村村民 {text} 獲勝!!!'.format(text = text))
            return 'winner'
        return False

    def save(self):
        self.redis_model.insert(self.room, self.data)

