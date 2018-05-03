import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from settings import *
show_corrcoef_plot = False
show_dif_plot = False
show_com_plot  = False
show_indiv_com_plot = True
corrcoef_window_size = 30    
time_between_difs = .5 #microseconds

def create_subplot_grid(num_charts):
    subplot_num_used = 0
    if num_charts == 1:
        subplot_num=[111]
        subplot_num_used = 0
    elif num_charts == 2:
        subplot_num=[212,211]
        subplot_num_used = 1
    elif num_charts == 3:
        subplot_num=[313,312,311]
        subplot_num_used = 2
    return subplot_num, subplot_num_used

def show_subplot(duration_at_end,index_multiplier,lines,subplot_num):
    interval = 5 #sets the plot ticks and the timer markers    
    tick_label,tick_index = [],[]
    plt.subplot(subplot_num)  
    for s in range(int(duration_at_end) + interval):
        if s%interval == 0:
            tick_label.append(s)
            tick_index.append(s*index_multiplier)
    index = 0        
    for line in lines:        
        labels = ['x0','y0','x1','y1','x2','y2','x3','y3','x4','y4','x5','y5','x6','y6','x7','y7','x8','y8','x9']                
        line1 = plt.plot(line, '.', label=labels[index])
        index = index + 1    
    plt.xticks(tick_index, tick_label, rotation='horizontal')
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

def make_dif_plot(duration_at_end, frames, subplot_num, subplot_num_used, time_between_difs):
    lines = []
    number_of_points = duration_at_end/time_between_difs
    print('number_of_points :'+str(number_of_points))
    for i in range(0,len(all_cx)): 
        frames_to_use_x = []
        frames_to_use_y = []
        all_time_dif_x = []
        all_time_dif_y = []
        for j in range(0,int(number_of_points)):
            index_to_use = int(max(0, min(len(all_cx[i])-1,(frames/number_of_points)*j)))            
            frames_to_use_x.append(all_cx[i][index_to_use])
            frames_to_use_y.append(all_cy[i][index_to_use])                               
            all_time_dif_x.append(frames_to_use_x[j]-frames_to_use_x[min(0,j-1)])
            all_time_dif_y.append(frames_to_use_y[j]-frames_to_use_y[min(0,j-1)])
        lines.append(all_time_dif_x)
        lines.append(all_time_dif_y)
    show_subplot(duration_at_end,int((len(all_time_dif_x)/duration_at_end)),lines,subplot_num[subplot_num_used])

def make_com_plot(duration,fps,all_cx, all_cy, subplot_num,subplot_num_used):
    lines = []
    for i in range(0,len(all_cx)):
        lines.append(all_cx[i])
        for a in range(0,len(all_cy[i])):
            all_cy[i][a] = frame_height-all_cy[i][a]
        lines.append(all_cy[i])
    average_x = []
    average_y = []
    for k in range(len(all_cx[0])):
        average_x.append(average_position(all_cx, 20, k))
        average_y.append(average_position(all_cy, 20, k))
    lines.append(average_x)
    lines.append(average_y)
    show_subplot(duration,fps,lines,subplot_num[subplot_num_used])

def make_indiv_com_plot(duration,fps,all_cx, all_cy,frame_height):
    subplot_num,subplot_num_used = create_subplot_grid(3)
    for i in range(0,len(all_cx)):
        lines = []
        lines.append(all_cx[i])
        for a in range(0,len(all_cy[i])):
            all_cy[i][a] = frame_height-all_cy[i][a]
        lines.append(all_cy[i])
        show_subplot(duration,fps,lines,subplot_num[min(len(subplot_num)-1,subplot_num_used)])
        subplot_num_used = subplot_num_used - 1 
    plt.show() 

def make_corrcoef_plot(duration_at_end,fps,all_cx, all_cy, subplot_num,subplot_num_used,corrcoef_window_size):
    lines = []
    window_x,window_y = deque(maxlen=corrcoef_window_size),deque(maxlen=corrcoef_window_size)
    for i in range(0,len(all_cx)):
        corrcoef_list = []
        for j in range(0,len(all_cx[i])):
            window_x.append(all_cx[i][j])
            window_y.append(all_cy[i][j])            
            if len(window_x) == corrcoef_window_size:            
                corrcoef_list.append(np.corrcoef(window_x,window_y)[0,1])
            else:
                corrcoef_list.append(0)
        lines.append(corrcoef_list)
    show_subplot(duration_at_end,fps,lines,subplot_num[subplot_num_used])

def create_plots(frames,start,end,frame_height):
    tick_label3,tick_index3,tick_label2,tick_index2,tick_label,tick_index = [],[],[],[],[],[]
    duration_at_end = end-start
    fps = frames/duration_at_end
    if show_indiv_com_plot:
        make_indiv_com_plot(duration_at_end,fps,all_cx, all_cy,frame_height) 
    num_charts = sum([show_dif_plot,show_com_plot,show_corrcoef_plot])    
    if num_charts > 0:
        subplot_num, subplot_num_used = create_subplot_grid(num_charts)
        if show_dif_plot:
            make_dif_plot(duration_at_end, frames, subplot_num, subplot_num_used, time_between_difs,all_cx)
            subplot_num_used = subplot_num_used - 1               
        if show_com_plot:
            make_com_plot(duration_at_end,fps,all_cx, all_cy, subplot_num,subplot_num_used)
            subplot_num_used = subplot_num_used - 1                             
        if show_corrcoef_plot:
            make_corrcoef_plot(duration_at_end,fps,all_cx, all_cy, subplot_num,subplot_num_used,corrcoef_window_size)
            subplot_num_used = subplot_num_used - 1
        plt.show()