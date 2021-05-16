import random

import numpy as np
import time
import sys

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

from tkinter import *
from PIL import Image, ImageTk

UNIT = 40  # pixels
POKEMON_H = 10  # grid height
POKEMON_W = 10  # grid width


class Pokemon(tk.Tk, object):
    def __init__(self):
        super(Pokemon, self).__init__()
        self.action_space = ['skill1', 'skill2', 'skill3', 'skill4', 'hp_up']
        self.n_actions = len(self.action_space)
        self.n_features = 7

        self.my_pokemon_name = '比卡超'
        self.skill_num = [30, 10, 20, 15]
        self.skill_current_num = [30, 10, 20, 15]
        self.skill_name = ['电击', '打雷', '抛摔', '十万伏特']
        self.skill_power = [80, 110, 80, 90]
        self.my_attack = 117
        self.my_defend = 101
        self.my_level = 50
        self.my_hp = 142

        self.enemy_pokemon_name = '超梦'
        self.enemy_skill_num = [25, 20, 10, 10]
        self.enemy_skill_current_num = [25, 20, 10, 10]
        self.enemy_skill_name = ['念力', '精神利刃', '精神强念', '精神击破']
        self.enemy_skill_power = [50, 70, 90, 100]

        # L100
        # self.enemy_attack = 202
        # self.enemy_defend = 166
        # self.enemy_level = 100
        # self.enemy_hp = 322

        # L70
        self.enemy_attack = 146
        self.enemy_defend = 142
        self.enemy_level = 70
        self.enemy_hp = 244

        self.enemy_action_space = [0, 1, 2, 3]

        self.hp_up = 100
        self.hp_up_num = 100
        self.hp_up_current_num = self.hp_up_num
        self.my_current_hp = self.my_hp
        self._my_current_hp = self.my_hp
        self.enemy_current_hp = self.enemy_hp
        self._enemy_current_hp = self.enemy_hp
        self.title('pokemon')
        self.geometry('{0}x{1}'.format(POKEMON_H * UNIT, POKEMON_H * UNIT))
        self.origin = np.array([20, 20])
        self.skill1_center = self.origin + np.array([UNIT * 0, UNIT * 5])
        self.skill2_center = self.origin + np.array([UNIT * 0, UNIT * 6])
        self.skill3_center = self.origin + np.array([UNIT * 0, UNIT * 7])
        self.skill4_center = self.origin + np.array([UNIT * 0, UNIT * 8])
        self.heal_center = self.origin + np.array([UNIT * 5, UNIT * 7])
        self.enemy_hp_center = self.origin + np.array([UNIT * 0 + 15, UNIT * 1])
        self.my_hp_center = self.origin + np.array([UNIT * 5, UNIT * 5])
        self.i_win = False
        self.enemy_win = False
        self.round = 0

        self._build_pokemon()

    def _build_pokemon(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=POKEMON_H * UNIT,
                                width=POKEMON_W * UNIT)

        # create pikachu
        self.im1 = Image.open("pikachu.png")
        self.im1 = self.im1.resize((150, 150), Image.ANTIALIAS)
        self.pikachu = ImageTk.PhotoImage(self.im1)
        self.canvas.create_image(self.skill1_center[0] - 5, self.skill1_center[1] - 100, anchor=NW, image=self.pikachu)
        # create enemy
        self.im2 = Image.open("enemy1.png")
        self.im2 = self.im2.resize((150, 150), Image.ANTIALIAS)
        self.enemy1 = ImageTk.PhotoImage(self.im2)
        self.canvas.create_image(self.origin[0] + 200, self.origin[1], anchor=NW, image=self.enemy1)

        self.whiteboard = self.canvas.create_rectangle(
            self.skill1_center[0] - 15, self.skill1_center[1] - 25,
            self.skill4_center[0] + 125, self.skill4_center[1] + 25,
            fill='white')
        # skill
        self.skill1 = self.canvas.create_rectangle(
            self.skill1_center[0] - 15, self.skill1_center[1] - 15,
            self.skill1_center[0] + 65, self.skill1_center[1] + 15,
            fill='white')
        # skill2
        self.skill2 = self.canvas.create_rectangle(
            self.skill2_center[0] - 15, self.skill2_center[1] - 15,
            self.skill2_center[0] + 65, self.skill2_center[1] + 15,
            fill='white')
        # skill3
        self.skill3 = self.canvas.create_rectangle(
            self.skill3_center[0] - 15, self.skill3_center[1] - 15,
            self.skill3_center[0] + 65, self.skill3_center[1] + 15,
            fill='white')
        # skill4
        self.skill4 = self.canvas.create_rectangle(
            self.skill4_center[0] - 15, self.skill4_center[1] - 15,
            self.skill4_center[0] + 65, self.skill4_center[1] + 15,
            fill='white')
        # heal
        self.heal = self.canvas.create_rectangle(
            self.heal_center[0] - 15, self.heal_center[1] - 15,
            self.heal_center[0] + 65, self.heal_center[1] + 15,
            fill='white')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            self.origin[0] - 15, self.origin[1] - 15,
            self.origin[0] + 45, self.origin[1] + 15,
            fill='red')

        # enemy hp
        self.canvas.create_rectangle(
            self.enemy_hp_center[0], self.enemy_hp_center[1] - 10,
                                     self.enemy_hp_center[0] + 145, self.enemy_hp_center[1] + 10,
            fill='white')
        self.hp = self.canvas.create_rectangle(
            self.enemy_hp_center[0], self.enemy_hp_center[1] - 10,
                                     self.enemy_hp_center[0] + 145, self.enemy_hp_center[1] + 10,
            fill='black', tags='eh')

        # my hp
        self.canvas.create_rectangle(
            self.my_hp_center[0] - 15, self.my_hp_center[1] + 10,
            self.my_hp_center[0] + 145, self.my_hp_center[1] + 30,
            fill='white')
        self.hp = self.canvas.create_rectangle(
            self.my_hp_center[0] - 15, self.my_hp_center[1] + 10,
            self.my_hp_center[0] + 145, self.my_hp_center[1] + 30,
            fill='black', tags='mh')

        # txt
        self.canvas.create_text(self.skill1_center[0] + 90, self.skill1_center[1],
                                text='%s / %s' % (self.skill_current_num[0], self.skill_num[0]), tags='1t')
        self.canvas.create_text(self.skill2_center[0] + 90, self.skill2_center[1],
                                text='%s / %s' % (self.skill_current_num[1], self.skill_num[1]), tags='2t')
        self.canvas.create_text(self.skill3_center[0] + 90, self.skill3_center[1],
                                text='%s / %s' % (self.skill_current_num[2], self.skill_num[2]), tags='3t')
        self.canvas.create_text(self.skill4_center[0] + 90, self.skill4_center[1],
                                text='%s / %s' % (self.skill_current_num[3], self.skill_num[3]), tags='4t')
        self.canvas.create_text(self.heal_center[0] + 90, self.heal_center[1],
                                text='%s / %s' % (self.hp_up_current_num, self.hp_up_num), tags='h')
        self.canvas.create_text(self.skill1_center[0] + 15, self.skill1_center[1], text=self.skill_name[0])
        self.canvas.create_text(self.skill2_center[0] + 15, self.skill2_center[1], text=self.skill_name[1])
        self.canvas.create_text(self.skill3_center[0] + 15, self.skill3_center[1], text=self.skill_name[2])
        self.canvas.create_text(self.skill4_center[0] + 15, self.skill4_center[1], text=self.skill_name[3])
        self.canvas.create_text(self.my_hp_center[0] + 20, self.my_hp_center[1],
                                text='%s：L%s' % (self.my_pokemon_name, self.my_level))
        self.canvas.create_text(self.enemy_hp_center[0] + 30, self.enemy_hp_center[1] - 20,
                                text='%s：L%s' % (self.enemy_pokemon_name, self.enemy_level))
        self.canvas.create_text(self.heal_center[0] + 15, self.heal_center[1], text='全满药')
        self.canvas.create_text(self.my_hp_center[0] - 35, self.my_hp_center[1] + 20, text='HP:')
        self.canvas.create_text(self.enemy_hp_center[0] - 20, self.enemy_hp_center[1], text='HP:')
        self.canvas.create_text(self.my_hp_center[0] + 90, self.my_hp_center[1] + 45,
                                text='(%s / %s)' % (self._my_current_hp, self.my_hp), tags='mhp')
        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        # time.sleep(1)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        skill1_center = origin + np.array([UNIT * 0, UNIT * 5])
        self.rect = self.canvas.create_rectangle(
            skill1_center[0] - 15, skill1_center[1] - 15,
            skill1_center[0] + 65, skill1_center[1] + 15,
            fill='red')

        self.enemy_current_hp = self._enemy_current_hp = self.enemy_hp
        self.my_current_hp = self._my_current_hp = self.my_hp
        self.skill_current_num = [30, 10, 20, 15]
        self.enemy_skill_current_num = [25, 20, 10, 10]
        self.hp_up_current_num = self.hp_up_num
        self.i_win = False
        self.enemy_win = False
        self.round = 0
        # return observation
        observation = [self.my_current_hp, self.enemy_current_hp,
                       self.skill_current_num[0], self.skill_current_num[1], self.skill_current_num[2],
                       self.skill_current_num[3],
                       self.hp_up_num];
        observation = np.array(observation);
        return observation

    def step(self, action):

        self.round += 1

        print('-----------第%s回合开始' % (self.round))
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])

        keepgoing = True
        # my pokemon logic
        if action == 0:  # skill 1
            if self.skill_current_num[0] == 0:
                keepgoing = False
                print('%s的%s已经用完(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[0], self.skill_current_num[0], self.skill_num[0]))
            else:
                self.skill_current_num[0] -= 1
                base_action[1] = self.skill1_center[1] - (s[1] + 15)
                hurt = self.get_hurt(self.my_level, self.my_attack, self.enemy_defend, self.skill_power[0])
                self._enemy_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[0], self.skill_current_num[0], self.skill_num[0]))
                print('伤害对方%s点血' % (hurt))
        elif action == 1:  # skill 2
            if self.skill_current_num[1] == 0:
                keepgoing = False
                print('%s的%s已经用完(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[1], self.skill_current_num[1], self.skill_num[1]))
            else:
                self.skill_current_num[1] -= 1
                base_action[1] = self.skill2_center[1] - (s[1] + 15)
                hurt = self.get_hurt(self.my_level, self.my_attack, self.enemy_defend, self.skill_power[1])
                self._enemy_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[1], self.skill_current_num[1], self.skill_num[1]))
                print('伤害对方%s点血' % (hurt))
        elif action == 2:  # skill 3
            if self.skill_current_num[2] == 0:
                keepgoing = False
                print('%s的%s已经用完(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[2], self.skill_current_num[2], self.skill_num[2]))
            else:
                self.skill_current_num[2] -= 1
                base_action[1] = self.skill3_center[1] - (s[1] + 15)
                hurt = self.get_hurt(self.my_level, self.my_attack, self.enemy_defend, self.skill_power[2])
                self._enemy_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[2], self.skill_current_num[2], self.skill_num[2]))
                print('伤害对方%s点血' % (hurt))
        elif action == 3:  # skill 4
            if self.skill_current_num[3] == 0:
                keepgoing = False
                print('%s的%s已经用完(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[3], self.skill_current_num[3], self.skill_num[3]))
            else:
                self.skill_current_num[3] -= 1
                base_action[1] = self.skill4_center[1] - (s[1] + 15)
                hurt = self.get_hurt(self.my_level, self.my_attack, self.enemy_defend, self.skill_power[3])
                self._enemy_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (
                    self.my_pokemon_name, self.skill_name[3], self.skill_current_num[3], self.skill_num[3]))
                print('伤害对方%s点血' % (hurt))
        elif action == 4:  # 补血
            if self.hp_up_current_num == 0:
                keepgoing = False
                print('%s的全满药已经用完' % (self.my_pokemon_name))
            else:
                self.hp_up_current_num -= 1
                base_action[1] = self.heal_center[1] - (s[1] + 15)
                # self._my_current_hp += self.hp_up
                # if self._my_current_hp > self.my_hp:
                #     self._my_current_hp = self.my_hp
                self._my_current_hp = self.my_hp  # 全满药
                print ('%s补血 %s(%s / %s)' % (self.my_pokemon_name,
                                             (self._my_current_hp - self.my_current_hp), self.hp_up_current_num,
                                             self.hp_up_num))

        if self._enemy_current_hp <= 0:
            self._enemy_current_hp = 0
            self.i_win = True
        if self.skill_current_num[0] == 0 and self.skill_current_num[1] == 0 and self.skill_current_num[2] == 0 and \
                        self.skill_current_num[3] == 0:
            self.enemy_win = True

        # enemy pokemon logic
        if keepgoing and not self.i_win:
            # enemy_action = random.sample(self.enemy_action_space, 1)[0]
            enemy_action = self.enemy_get_action()
            if enemy_action == 0:
                self.enemy_skill_current_num[0] -= 1
                hurt = self.get_hurt(self.enemy_level, self.enemy_attack, self.my_defend, self.enemy_skill_power[0])
                self._my_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (self.enemy_pokemon_name,
                                            self.enemy_skill_name[0], self.enemy_skill_current_num[0],
                                            self.enemy_skill_num[0]))
                print('伤害我方%s点血' % (hurt))
                if self.enemy_skill_current_num[0] <= 0:
                    print('%s的%s已经用完(%s / %s)' % (self.enemy_pokemon_name,
                                                  self.enemy_skill_name[0], self.enemy_skill_current_num[0],
                                                  self.enemy_skill_num[0]))
            elif enemy_action == 1:
                self.enemy_skill_current_num[1] -= 1
                hurt = self.get_hurt(self.enemy_level, self.enemy_attack, self.my_defend, self.enemy_skill_power[1])
                self._my_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (self.enemy_pokemon_name,
                                            self.enemy_skill_name[1], self.enemy_skill_current_num[1],
                                            self.enemy_skill_num[1]))
                print('伤害我方%s点血' % (hurt))
                if self.enemy_skill_current_num[1] <= 0:
                    print('%s的%s已经用完(%s / %s)' % (self.enemy_pokemon_name,
                                                  self.enemy_skill_name[1], self.enemy_skill_current_num[1],
                                                  self.enemy_skill_num[1]))
            elif enemy_action == 2:
                self.enemy_skill_current_num[2] -= 1
                hurt = self.get_hurt(self.enemy_level, self.enemy_attack, self.my_defend, self.enemy_skill_power[2])
                self._my_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (self.enemy_pokemon_name,
                                            self.enemy_skill_name[2], self.enemy_skill_current_num[2],
                                            self.enemy_skill_num[2]))
                print('伤害我方%s点血' % (hurt))
                if self.enemy_skill_current_num[2] <= 0:
                    print('%s的%s已经用完(%s / %s)' % (self.enemy_pokemon_name,
                                                  self.enemy_skill_name[2], self.enemy_skill_current_num[2],
                                                  self.enemy_skill_num[2]))
            elif enemy_action == 3:
                self.enemy_skill_current_num[3] -= 1
                hurt = self.get_hurt(self.enemy_level, self.enemy_attack, self.my_defend, self.enemy_skill_power[3])
                self._my_current_hp -= hurt
                print('%s使出了%s(%s / %s)' % (self.enemy_pokemon_name,
                                            self.enemy_skill_name[3], self.enemy_skill_current_num[3],
                                            self.enemy_skill_num[3]))
                print('伤害我方%s点血' % (hurt))
                if self.enemy_skill_current_num[3] <= 0:
                    print('%s的%s已经用完(%s / %s)' % (self.enemy_pokemon_name,
                                                  self.enemy_skill_name[3], self.enemy_skill_current_num[3],
                                                  self.enemy_skill_num[3]))
        elif not keepgoing:
            self.round -= 1

        if self._my_current_hp <= 0:
            self._my_current_hp = 0
            self.enemy_win = True

        if not self.enemy_win:
            if self.enemy_skill_current_num[0] <= 0 and self.enemy_skill_current_num[1] <= 0 and \
                            self.enemy_skill_current_num[2] <= 0 and self.enemy_skill_current_num[3] <= 0:
                print('%s全部招式用完' % (self.enemy_pokemon_name))
                self.i_win = True

        self.canvas.move(self.rect, 0, base_action[1])  # move agent

        self.canvas.delete("eh")
        self.hp = self.canvas.create_rectangle(
            self.enemy_hp_center[0], self.enemy_hp_center[1] - 10,
                                     self.enemy_hp_center[0] + 145 * round(self.enemy_current_hp / self.enemy_hp, 2),
                                     self.enemy_hp_center[1] + 10,
            fill='black', tags='eh')

        self.canvas.delete("mh")
        self.hp = self.canvas.create_rectangle(
            self.my_hp_center[0] - 15, self.my_hp_center[1] + 10,
            self.my_hp_center[0] - 15 + 135 * round(self.my_current_hp / self.my_hp, 2), self.my_hp_center[1] + 30,
            fill='black', tags='mh')

        # skill 1 num
        self.canvas.delete("1t")
        self.canvas.create_text(self.skill1_center[0] + 90, self.skill1_center[1],
                                text='%s / %s' % (self.skill_current_num[0], self.skill_num[0]), tags='1t')
        # skill 2 num
        self.canvas.delete("2t")
        self.canvas.create_text(self.skill2_center[0] + 90, self.skill2_center[1],
                                text='%s / %s' % (self.skill_current_num[1], self.skill_num[1]), tags='2t')
        # skill 3 num
        self.canvas.delete("3t")
        self.canvas.create_text(self.skill3_center[0] + 90, self.skill3_center[1],
                                text='%s / %s' % (self.skill_current_num[2], self.skill_num[2]), tags='3t')
        # skill 4 num
        self.canvas.delete("4t")
        self.canvas.create_text(self.skill4_center[0] + 90, self.skill4_center[1],
                                text='%s / %s' % (self.skill_current_num[3], self.skill_num[3]), tags='4t')
        # heal num
        self.canvas.delete("h")
        self.canvas.create_text(self.heal_center[0] + 90, self.heal_center[1],
                                text='%s / %s' % (self.hp_up_current_num, self.hp_up_num), tags='h')
        # my hp
        self.canvas.delete("mhp")
        self.canvas.create_text(self.my_hp_center[0] + 90, self.my_hp_center[1] + 45,
                                text='(%s / %s)' % (self._my_current_hp, self.my_hp), tags='mhp')

        more_reward = 0
        if action == 4 and self.hp_up_current_num > 0 and (self.my_current_hp / self.my_hp) < 0.63:
            more_reward = 800
        elif (self.my_current_hp / self.my_hp) >= 0.63 and action in (0, 1, 2, 3):
            more_reward = 800
        reward = 1 * (self._my_current_hp - self.my_current_hp) - 1 * (self._enemy_current_hp - self.enemy_current_hp) \
                 + more_reward

        self.enemy_current_hp = self._enemy_current_hp
        self.my_current_hp = self._my_current_hp

        print('***我方血量：(%s / %s)' % (self._my_current_hp, self.my_hp))
        print('***敌方血量：(%s / %s)' % (self._enemy_current_hp, self.enemy_hp))

        s_ = [self.my_current_hp, self.enemy_current_hp,
              self.skill_current_num[0], self.skill_current_num[1], self.skill_current_num[2],
              self.skill_current_num[3],
              self.hp_up_current_num];
        s_ = np.array(s_);
        # print('s_:',s_)
        print('~~~~~~~~~~~第%s回合结束，奖励:%s' % (self.round, reward))

        if self.i_win:
            reward += 1200
            done = True
            print('%s赢了' % (self.my_pokemon_name))
            print('奖励:%s' % (reward))
            print('-----------------------------------------------------------------------')
        elif self.enemy_win:
            reward -= 1200
            done = True
            print('%s赢了' % (self.enemy_pokemon_name))
            print('奖励:%s' % (reward))
            print('-----------------------------------------------------------------------')
        else:
            done = False

        return s_, reward, done, ''

    def enemy_get_action(self):
        enemy_action = random.sample(self.enemy_action_space, 1)[0]
        if self.enemy_skill_current_num[0] > 0 or self.enemy_skill_current_num[1] > 0 or self.enemy_skill_current_num[
            2] > 0 or self.enemy_skill_current_num[3] > 0:
            while (self.enemy_skill_current_num[enemy_action] <= 0):
                enemy_action += 1
                if enemy_action >= 4:
                    enemy_action = 0
        return enemy_action

    def get_hurt(self, level, my_attack, enemy_defend, power):
        hurt = ((2 * level + 10) / 250) * (my_attack / enemy_defend) * power + 2
        return hurt

    def render(self):
        # time.sleep(1)
        self.update()
