import math
import sys

import numpy as np
import pygame
from pygame import Vector3, Vector2


class Vector4:
    def __init__(self, x, y, z, w) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z}, {self.w})"
    
    def __getitem__(self, i):
        return [self.x, self.y, self.z, self.w][i]

    def normalize(self):
        if self.w == 0:
            self.x = float('inf')
            self.y = float('inf')
            self.z = float('inf')
            self.w = float('inf')
            return
        self.x = self.x / self.w
        self.y = self.y / self.w
        self.z = self.z / self.w
        self.w = self.w / self.w
    
    @property
    def xyz(self) -> Vector3:
        return Vector3(self.x, self.y, self.z)

def convert_list_to_vector(v):
    if len(v) == 2:
        return Vector2(*v)
    if len(v) == 3:
        return Vector3(*v)
    if len(v) == 4:
        return Vector4(*v)

class mat:
    def __init__(self, values:list) -> None:
        self.v = values

    def rows(self):
        return len(self.v)

    def columns(self):
        return len(self.v[0])

    def __str__(self) -> str:
        rows = self.rows()
        columns = self.columns()
        return "\n".join([" ".join([f"{self.v[a][b]:.2f}" for b in range(columns)]) for a in range(rows)])
    
    def __mul__(self, other):
        if type(other) == mat:
            assert self.columns() == other.rows()

            v = [[0 for _ in range(self.rows())] for _ in range(other.columns())]

            for r in range(self.rows()):
                for c in range(other.columns()):
                    for k in range(other.rows()):
                        v[r][c] += self.v[r][k] * other.v[k][c]
                    
            return mat(v)

        elif type(other) == Vector3:
            assert(self.columns() == 3)
            output = [0 for _ in range(self.rows())]
            for r in range(self.rows()):
                for c in range(self.columns()):
                    output[r] += self.v[r][c] * other[c]
            return convert_list_to_vector(v)
        
        elif type(other) == Vector4:
            assert(self.columns() == 4)
            output = [0 for _ in range(self.rows())]
            for r in range(self.rows()):
                for c in range(self.columns()):
                    output[r] += self.v[r][c] * other[c]
            return convert_list_to_vector(output)
        else:
            assert(False)
    
    def inv(self):
        a = np.linalg.inv(self.v)
        return mat([[y for y in x] for x in a])
    
    def set_size(self, rows, columns):
        while self.rows() > rows:
            self.v.pop(-1)
        while self.rows() < rows:
            new_row = self.rows()
            self.v.append([1.0 if i == new_row else 0.0 for i in range(self.columns())])
        
        while self.columns() > columns:
            for i in range(self.rows()):
                self.v[i].pop(-1)
        while self.columns() < columns:
            new_columns = self.columns()
            for i in range(self.rows()):
                self.v[i].append(1.0 if i == new_columns else 0.0)
    
    def all_values(self):
        return [j for i in self.v for j in i]


def translation_mat(v:Vector3)->mat:
    return mat([
        [1.0, 0.0, 0.0, v.x],
        [0.0, 1.0, 0.0, v.y],
        [0.0, 0.0, 1.0, v.z],
        [0.0, 0.0, 0.0, 1.0],
    ])

def vec3_to_vec4(v:Vector3):
    return Vector4(v.x, v.y, v.z, 1.0)

def rotation_mat(v:Vector3)->mat:
    c_x = math.cos(v.x)
    c_y = math.cos(v.y)
    c_z = math.cos(v.z)

    s_x = math.sin(v.x)
    s_y = math.sin(v.y)
    s_z = math.sin(v.z)
    
    rotate_x = mat([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, c_x,-s_x, 0.0],
            [0.0, s_x, c_x, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    rotate_y = mat([
            [c_y, 0.0,-s_y, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [s_y, 0.0, c_y, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    rotate_z = mat([
            [c_z,-s_z, 0.0, 0.0],
            [s_z, c_z, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    return rotate_x * rotate_y *  rotate_z

class canvas:
    def __init__(self, init_data) -> None:
        if type(init_data) == tuple:
            pygame.init()
            self.screen = pygame.display.set_mode(init_data)
            self.width, self.height = self.size = init_data
        elif type(init_data) == pygame.Surface:
            self.screen = init_data
            self.width, self.height = self.screen.get_width(), self.screen.get_height()

    def set_projection(self, m:mat):
        self.projection_matrix = m
    
    def set_view(self, m:mat):
        self.view_matrix = m
    
    def update_events(self):
        self.mouse_move = Vector2()
        self.pressed_keys = []

        for event in pygame.event.get():

            if event.type == pygame.QUIT: 
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.append(event.key)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_move = Vector2(event.rel).elementwise() / Vector2(self.width, self.width).elementwise()

    def get_new_pressed_keys(self): 
        # print(self.pressed_keys)
        return self.pressed_keys
    
    def is_pressed(self, k)->bool:
        keys = pygame.key.get_pressed()
        keys = [i for i, x in enumerate(keys) if x]
        result = k in keys
        return result

    def is_left_button_down(self):
        return pygame.mouse.get_pressed(3)[0]

    def is_right_button_down(self):
        return pygame.mouse.get_pressed(3)[2]
    
    def get_mouse_move(self)->Vector2:
        return self.mouse_move

    def clear(self, color):
        self.screen.fill(color)
    
    def present(self):
        pygame.display.flip() 

    def project_point(self, v:Vector3) -> Vector3:
        p = Vector3(v.x, -v.y, v.z)
        p = self.projection_matrix * self.view_matrix * vec3_to_vec4(p)
        p.normalize()
        p = Vector3((p.x * 0.5 + 0.5) * self.width, (1.0 - (p.y * 0.5 + 0.5)) * self.height, p.z)
        return p
    
    def draw_sphere(self, p:Vector3, resolution = 20, radius = 1.0, line_width = 2, color = (255, 0, 0)):
        #draw ring
        diameter = radius
        points = []
        for ii in range(resolution):
            a = (ii / resolution) * 2 * math.pi
            points.append(self.project_point(p + diameter * Vector3(math.cos(a), 0.0, math.sin(a))).xy)
        pygame.draw.polygon(self.screen, color, points, width=line_width)

        #draw X
        points = []
        for ii in range(resolution):
            a = (ii / resolution) * 2 * math.pi
            points.append(self.project_point(p + diameter * Vector3(0.0, math.cos(a), math.sin(a))).xy)
        pygame.draw.lines(self.screen, color, points=points, width=line_width, closed=False)
        
        #draw Z
        points = []
        for ii in range(resolution):
            a = (ii / resolution) * 2 * math.pi
            points.append(self.project_point(p + diameter * Vector3(math.cos(a), -math.sin(a), 0.0)).xy)
        pygame.draw.lines(self.screen, color, points=points, width=line_width, closed=False)

    def draw_hemisphere(self, p:Vector3, resolution = 20, radius = 1.0, line_width = 2, color = (255, 0, 0)):
        #draw ring
        diameter = radius * 2
        points = []
        for ii in range(resolution):
            a = (ii / resolution) * 2 * math.pi
            points.append(self.project_point(p + diameter * Vector3(math.cos(a), 0.0, math.sin(a))).xy)
        pygame.draw.polygon(self.screen, color, points, width=line_width)

        #draw X
        points = []
        for ii in range(resolution):
            a = (ii / (resolution-1)) * math.pi - math.pi * 1/2
            points.append(self.project_point(p + diameter * Vector3(0.0, math.cos(a), math.sin(a))).xy)
        pygame.draw.lines(self.screen, color, points=points, width=line_width, closed=False)
        
        #draw Z
        points = []
        for ii in range(resolution):
            a = (ii / (resolution-1)) * math.pi + math.pi
            points.append(self.project_point(p + diameter * Vector3(math.cos(a), -math.sin(a), 0.0)).xy)
        pygame.draw.lines(self.screen, color, points=points, width=line_width, closed=False)
    
    def draw_cylinder(self, p:Vector3, color = (255, 0, 0), resolution = 20, diameter = 1.0, height = 1.0, line_width = 2):
        #draw ring
        if self.is_outside(self.project_point(p)):
            return
        bottom_ring = []
        top_ring = []
        for ii in range(resolution):
            a = (ii / resolution) * 2 * math.pi
            new_p = p + diameter * Vector3(math.cos(a), 0.0, math.sin(a))
            bottom_ring.append(self.project_point(                            new_p).xy)
            top_ring.append(   self.project_point(Vector3(0.0, height, 0.0) + new_p).xy)
        pygame.draw.polygon(self.screen, color, bottom_ring, width=line_width)
        pygame.draw.polygon(self.screen, color, top_ring, width=line_width)

        pygame.draw.line(self.screen, color, bottom_ring[int(resolution * 0/4)], top_ring[int(resolution * 0/4)], width=line_width)
        pygame.draw.line(self.screen, color, bottom_ring[int(resolution * 1/4)], top_ring[int(resolution * 1/4)], width=line_width)
        pygame.draw.line(self.screen, color, bottom_ring[int(resolution * 2/4)], top_ring[int(resolution * 2/4)], width=line_width)
        pygame.draw.line(self.screen, color, bottom_ring[int(resolution * 3/4)], top_ring[int(resolution * 3/4)], width=line_width)
    

    def is_outside(self, p:Vector3):
        return p.z >= 0 or p.x < 0 or p.x > self.width or p.y < 0 or p.y > self.height
            
    Vector3s = list[Vector3]
    def draw_lines(self, points:Vector3s, color = (255, 0, 0), line_width = 2, closed=False):
        if len(points) == 0:
            return

        center = Vector3(0.0,0.0,0.0)
        for p in points:
            center += p
        center = center / len(points)
        
        projected_center = self.project_point(center)
        if self.is_outside(projected_center):
            return

        new_p = [self.project_point(p).xy for p in points]
        pygame.draw.lines(self.screen, color=color, points=new_p, width=line_width, closed=closed)
    
    def draw_point(self, point:Vector3, color = (255, 0, 0), radius = 2, line_width = 2):
        p = self.project_point(point)
        if self.is_outside(p):
            return
        
        pygame.draw.circle(self.screen, color=color, center=p.xy, radius=radius, width=line_width) 

    def draw_cube(self, position:Vector3, scale:Vector3 = Vector3(1.0,1.0,1.0), rotation:Vector3 = Vector3(0.0,0.0,0.0), offset:Vector3 = Vector3(0.0,0.0,0.0), color = (255, 0, 0), line_width = 2):
        points = [
            Vector3(-0.5, -0.5, -0.5),
            Vector3(-0.5, -0.5,  0.5),
            Vector3( 0.5, -0.5,  0.5),
            Vector3( 0.5, -0.5, -0.5),
            
            Vector3( 0.5,  0.5, -0.5),
            Vector3(-0.5,  0.5, -0.5),
            Vector3(-0.5,  0.5,  0.5),
            Vector3( 0.5,  0.5,  0.5),
        ]

        r = rotation_mat(rotation)

        for i, p in enumerate(points):
            p = p.elementwise() * scale.elementwise()
            p = (r * vec3_to_vec4(p)).xyz
            p = p + position + offset
            points[i] = p 
        
        # draw_points = points + [points[4], points[7], points[2], points[1], points[6], points[5], points[0]]
        bottom = points[0:4]
        top = points[4:8]
        left = points[0:2]  + points[6:7] + points[5:6]
        right = points[2:4] + points[4:5] + points[7:8] 

        self.draw_lines(bottom, color=color, line_width=line_width, closed=True)
        self.draw_lines(top, color=color, line_width=line_width, closed=True)
        self.draw_lines(left, color=color, line_width=line_width, closed=True)
        self.draw_lines(right, color=color, line_width=line_width, closed=True)
