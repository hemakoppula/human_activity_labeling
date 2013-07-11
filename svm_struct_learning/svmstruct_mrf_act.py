"""A module for SVM^python for multiclass MRF learning."""
import random

# Hema Koppula, hema@cs.cornell.edu

import numpy
import sys
from numpy import random
import time
from operator import concat
import svmapi, array
import commands
from numpy import *
import scipy as Sci
import scipy.linalg
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix
from numpy.ma.core import zeros
import glpk
from bitarray import bitarray
from graphcut import *
from scipy.sparse.coo import coo_matrix

global NUM_CLASSES_OBJ
global NUM_CLASSES_SKEL
global NUM_CLASSES
global ITER
global LP_LIST
global LOSS_WEIGHTS
global LOSS_METHOD
global SINGLE_FRAME
global TEMPORAL
global NODEONLY

LP_LIST= []
ITER = 0
NUM_CLASSES = 0
# default options
LOSS_METHOD = "micro"
TEMPORAL = "false"
NODEONLY = "false"

def get_C_matrix(num_node_feats, num_edge_feats, num_ass_edge_feats, K ):
    num_nonass_edge_feats = num_edge_feats - num_ass_edge_feats;
    num_ones = num_node_feats*K + num_ass_edge_feats*K + num_nonass_edge_feats*K*K;
    crow = zeros(num_ones)
    ccol = zeros(num_ones)
    cval = ones(num_ones)

    index = 0;
    for l in xrange(0,num_node_feats*K):
        crow[index] = l
        ccol[index] = l
        index = index + 1

    for l in xrange(0,K):
        for i in xrange(0,num_ass_edge_feats):
            crow[index] = (num_ass_edge_feats*l + i) + num_node_feats*K
            ccol[index] = (num_edge_feats*(l*K+l) + i) +  num_node_feats*K
            index += 1

    for l in xrange(0,K):
        for k in xrange(0, K):
            for i in xrange(0,num_nonass_edge_feats):
                crow[index] =   num_node_feats*K+ (num_ass_edge_feats*K + num_nonass_edge_feats*(l*K+k)+i )
                ccol[index] =   num_node_feats*K+ (num_edge_feats*(l*K+k) + num_ass_edge_feats + i)
                index +=1


    C = csr_matrix((cval,(crow,ccol)),shape=(num_node_feats*K + num_ass_edge_feats*K + num_nonass_edge_feats*K*K , num_node_feats*K + (num_edge_feats*K*K)),dtype='d')
    return C

def get_C_obj_matrix(num_node_feats, num_edge_feats, num_ass_edge_feats, K, objMapList ):

    partialSums = [0]

    num_ass_terms = 0;
    for l in objMapList:
        num_ass_terms += len(l)*len(l)
        partialSums.append(num_ass_terms)

    num_nonass_edge_feats = num_edge_feats - num_ass_edge_feats;
    num_ones = num_node_feats*K + num_ass_edge_feats*num_ass_terms + num_nonass_edge_feats*K*K;
    crow = zeros(num_ones)
    ccol = zeros(num_ones)
    cval = ones(num_ones)

    index = 0;
    for l in xrange(0,num_node_feats*K):
        crow[index] = l
        ccol[index] = l
        index = index + 1
    
    objCnt = -1
    for o in objMapList:
        objCnt +=1;
        num_parts = len(o)
        for pl in xrange(0,num_parts):
            for pk in xrange(0,num_parts):
                for i in xrange(0,num_ass_edge_feats):
                    crow[index] = num_ass_edge_feats*(partialSums[objCnt] + pl*num_parts + pk) + i + num_node_feats*K
                    #print pl , pl , num_parts, partialSums[objCnt], objCnt, crow[index]
                    assert crow[index] < num_ones
                    
                    ccol[index] = num_edge_feats*( (int(o[pl])-1)*K+ (int(o[pk])-1) ) + i +  num_node_feats*K
                    index += 1

    for l in xrange(0,K):
        for k in xrange(0, K):
            for i in xrange(0,num_nonass_edge_feats):
                crow[index] =   num_node_feats*K+ (num_ass_edge_feats*num_ass_terms + num_nonass_edge_feats*(l*K+k)+i )
                
                assert crow[index] < num_ones
                ccol[index] =   num_node_feats*K+ (num_edge_feats*(l*K+k) + num_ass_edge_feats + i)
                index +=1

    

    C = csr_matrix((cval,(crow,ccol)),shape=(num_node_feats*K + num_ass_edge_feats*num_ass_terms + num_nonass_edge_feats*K*K , num_node_feats*K + (num_edge_feats*K*K)),dtype='d')
    return C

def parse_parameters(sparm):
    temp_arg_list = sparm.argv
    print sparm.argv
    global LOSS_METHOD
    global SINGLE_FRAME
    global TEMPORAL
    global NODEONLY
    # set default values
    LOSS_METHOD = "micro"
    for i in xrange(0,len(sparm.argv)/2):
        #print i,  len(sparm.argv)/2
        opt = temp_arg_list.pop(0)
        val = temp_arg_list.pop(0)
        if(opt == "--l"):
            LOSS_METHOD = val
        if(opt == "--am"):
            print "setting am to ", val
        if(opt == "--sf"):
            SINGLE_FRAME= val
        if(opt == "--temporal"):
            TEMPORAL= val
        if(opt == "--nodeonly"):
            NODEONLY = val



def parse_parameters_classify(attribute, value):
    
    global LOSS_METHOD
    global SINGLE_FRAME
    global TEMPORAL
    global NODEONLY
    # set default values
    #print attribute, value
    if(attribute == "--l"):
        LOSS_METHOD = value
    if(attribute == "--sf"):
        SINGLE_FRAME= value
    if(attribute == "--temporal"):
        TEMPORAL= value
    if(attribute == "--nodeonly"):
        NODEONLY= value


def read_examples(filename,sparm):
    global SINGLE_FRAME
    examples = []
    if(SINGLE_FRAME == "true"):
        examples = read_examples_single_frame(filename, sparm)
    else:
        examples = read_examples_multiple_frames(filename, sparm)
    return examples


def read_examples_multiple_frames(filename,sparm):
    global TEMPORAL
    global NUM_CLASSES
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
     # Helper function for reading from files.
    def line_reader(lines):
        # returns only non-empty lines
        # strips comments (anything after '#')
        for l in lines:
            i = l.find('#')
            if i == -1: yield l.strip()


    """Parses an input file into an example sequence."""
    # This reads example files of the type read by SVM^multiclass.
    examples = []
    max_target=0
    num_obj_feats=0
    num_skel_feats=0
    num_obj_t_feats=0
    num_skel_t_feats=0
    num_obj_obj_feats=0
    num_obj_skel_feats=0


    start = time.clock()

    # Open the file and read each example.
    for input_file in file(filename):
        files = [line.split() for line in line_reader(file(input_file.strip()))]
        print files
        print input_file
        for frame_num in xrange(1,int(files[0][0].strip())):
            frame_file = files[frame_num][0].strip()
            print frame_file
            input = [line.split() for line in line_reader(file(frame_file.strip()))]
        # first line has the number of nodes and number of edges
            N1 = int(input[0][0].strip())
            N2 = 1
            if(NODEONLY == "true"):
                N2 =  0
            E1 = int(input[0][1].strip())
            E2 = int(input[0][2].strip())
            K1 = int(input[0][3].strip())
            K2 = int(input[0][4].strip())

            # find the max class and number of node features -- will work for sparse representation
            for i in xrange(0,N1):
                tokens = [line.split(':') for line in input[i+1][2:]]
                for k,v in tokens:
                    if(num_obj_feats<int(k)):
                        num_obj_feats=int(k)
            for i in xrange(N1, N1+N2):
                tokens = [line.split(':') for line in input[i+1][2:]]
                for k,v in tokens:
                    if(num_skel_feats<int(k)):
                        num_skel_feats=int(k)
            for i in xrange(N1+N2, N1+N2+E1):
                tokens = [line.split(':') for line in input[i+1][4:]]
                for k,v in tokens:
                    if(num_obj_obj_feats<int(k)):
                        num_obj_obj_feats=int(k)
            for i in xrange(N1+N2+E1,N1+N2+E1+E2):
                tokens = [line.split(':') for line in input[i+1][3:]]
                for k,v in tokens:
                    if(num_obj_skel_feats<int(k)):
                        num_obj_skel_feats=int(k)
        if(TEMPORAL == "true"):
            for edge_num in xrange(1+int(files[0][0].strip()),1+int(files[0][0].strip())+int(files[0][1].strip())):
                edge_file = files[edge_num][0].strip()
                print edge_file
                input = [line.split() for line in line_reader(file(edge_file.strip()))]
                E3 = int(input[0][0].strip())
                E4 = int(input[0][1].strip())
                for i in xrange(0,E3):
                    tokens = [line.split(':') for line in input[i+1][3:]]
                    for k,v in tokens:
                        if(num_obj_t_feats<int(k)):
                            num_obj_t_feats=int(k)
                for i in xrange(E3,E3+E4):
                    tokens = [line.split(':') for line in input[i+1][3:]]
                    for k,v in tokens:
                        if(num_skel_t_feats<int(k)):
                            num_skel_t_feats=int(k)

    max_obj_target = K1 # use the max number of classes read from the file
    max_skel_target = K2
    NUM_CLASSES_OBJ = K1
    NUM_CLASSES_SKEL = K2

    print 'number of obj classes: ', max_obj_target
    print 'number of skel classes: ', max_skel_target

    print 'number of obj features: ', num_obj_feats
    print 'number of skel features: ', num_skel_feats
    print 'number of obj obj edge features: ',num_obj_obj_feats
    print 'number of obj skel edge features: ',num_obj_skel_feats
    print 'number of obj temporal edge features: ',num_obj_t_feats
    print 'number of obj temporal edge features: ',num_skel_t_feats

    print 'time spent in preprocessing data files', start-time.clock()


    class_counts = zeros(K1+K2)
    frame_count = 0
    temporal_edge_count = 0
    X_multiple = []
    Y_multiple = []
    X_temporal = []
    Y_temporal = []
    edges_obj_obj_list = []
    edges_obj_skel_list = []
    edges_obj_temporal_list = []
    temporal_frames_list = []
    N1_list = []
    E_list = []
    obj_map_list = []
    frame_map = {}
    example_num=-1
    for input_file in file(filename):
        files = [line.split() for line in line_reader(file(input_file.strip()))]
        print input_file
        X_multiple = []
        Y_multiple = []
        X_temporal = []
        Y_temporal = []
        frame_count = 0
        frame_map = {}
        obj_map_list = []
        edges_obj_obj_list = []
        edges_obj_skel_list = []
        N1_list = []
        E_list = []
        example_num+=1
        for frame_num in xrange(1,int(files[0][0].strip())+1):
            frame_file = files[frame_num][0].strip()
            print frame_file
            frame_count +=1
            input = [line.split() for line in line_reader(file(frame_file.strip()))]
            # first line has the number of nodes and number of edges
            N1 = int(input[0][0].strip());
            N2 = 1
            if(NODEONLY == "true"):
                N2 =  0
            E1 = int(input[0][1].strip());
            E2 = int(input[0][2].strip());
            FN = int(input[0][5].strip());
            xrow = zeros(N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats  + E1*max_obj_target*max_obj_target*num_obj_obj_feats + E2*max_obj_target*max_skel_target*num_obj_skel_feats )
            xcol = zeros(N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats  + E1*max_obj_target*max_obj_target*num_obj_obj_feats + E2*max_obj_target*max_skel_target*num_obj_skel_feats)
            xval = zeros(N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats  + E1*max_obj_target*max_obj_target*num_obj_obj_feats + E2*max_obj_target*max_skel_target*num_obj_skel_feats)
            #Xn= mat(zeros((max_target * num_node_feats,max_target*N)));
            Yn= mat(zeros((max_obj_target*N1+max_skel_target*N2,1)))

        #XY_test = mat(zeros((max_target*num_node_feats + max_target*max_target*num_edge_feats,1)))
            obj_map = {}

            for i in xrange(0,N1):
                target = int(input[i+1][0]);
                if(target != -1): # if the segment is unlabeled all entries of Yn for the label will be 0
                    #print target
                    class_counts[target-1]+=1
                    Yn[i*max_obj_target+(target-1),0]=1

                # get the segment number
                obj_map[int(input[i+1][1])] = i

                # Get the features.
                tokens = [line.split(':') for line in input[i+1][2:]]

                # assumes all features are present
                features = mat([float(v) for k,v in tokens])
                #print features
                f = features.transpose()

                # fill in the Xn matrix
                for j in xrange(0,max_obj_target):
                    xval[(i*max_obj_target+j)*num_obj_feats:(i*max_obj_target+j+1)*num_obj_feats] = features.A[0];
                    for v in xrange(0,num_obj_feats):
                        xrow[(i*max_obj_target+j)*num_obj_feats+v] = j*num_obj_feats+v
                    xcol[(i*max_obj_target+j)*num_obj_feats:(i*max_obj_target+j+1)*num_obj_feats] = i*max_obj_target+(j)
            #skel nodes
            for i in xrange(0, N2):
                target = int(input[N1+i+1][0]);
                print target
                if(target != -1): # if the segment is unlabeled all entries of Yn for the label will be 0
                    Yn[N1*max_obj_target + i*max_skel_target+(target-1),0]=1

                   # Get the features.
                tokens = [line.split(':') for line in input[N1+i+1][2:]]

                # assumes all features are present
                features = mat([float(v) for k,v in tokens])
                #print features
                f = features.transpose()

                # fill in the Xn matrix
                for j in xrange(0,max_skel_target):
                    xval[N1*max_obj_target*num_obj_feats+(i*max_skel_target+j)*num_skel_feats:N1*max_obj_target*num_obj_feats+(i*max_skel_target+j+1)*num_skel_feats] = features.A[0];
                    for v in xrange(0,num_skel_feats):
                        xrow[N1*max_obj_target*num_obj_feats+(i*max_skel_target+j)*num_skel_feats+v] = max_obj_target*num_obj_feats + j*num_skel_feats+v
                    xcol[N1*max_obj_target*num_obj_feats + (i*max_skel_target+j)*num_skel_feats : N1*max_obj_target*num_obj_feats + (i*max_skel_target+j+1)*num_skel_feats] = N1*max_obj_target + i*max_skel_target+(j)

            edges_obj_obj = mat(zeros((E1,2)))
            Ye1 = mat(zeros((max_obj_target*max_obj_target*E1,1)))
            for i in xrange(N1+N2,N1+N2+E1):
                target1 = int(input[i+1][0]);
                target2 = int(input[i+1][1]);
                if(target1 != -1 and target2 != -1): # both should be labeled to add to Ye
                    Ye1[(i-(N1+N2))*max_obj_target*max_obj_target + (target1-1)*max_obj_target+(target2-1)]=1
                # get the segment numbers
                edges_obj_obj[i-(N1+N2),0]= obj_map[int(input[i+1][2])]
                edges_obj_obj[i-(N1+N2),1]= obj_map[int(input[i+1][3])]

                tokens = [line.split(':') for line in input[i+1][4:]]
                features = mat([float(v) for k,v in tokens])
            #print features
                f = features.transpose()

            # fill in the Xn matrix
                S = N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats
                for j in xrange(0,max_obj_target*max_obj_target):
                    xval[S + ((i-(N1+N2))*max_obj_target*max_obj_target+j)*num_obj_obj_feats: S + ((i-(N1+N2))*max_obj_target*max_obj_target+(j+1))*num_obj_obj_feats] = features.copy();
                    for v in xrange(0,num_obj_obj_feats):
                        xrow[S+((i-(N1+N2))*max_obj_target*max_obj_target+j)*num_obj_obj_feats+v] = max_obj_target*num_obj_feats + max_skel_target*num_skel_feats + j*num_obj_obj_feats+v
                    xcol[S + ((i-(N1+N2))*max_obj_target*max_obj_target+j)*num_obj_obj_feats: S + ((i-(N1+N2))*max_obj_target*max_obj_target+(j+1))*num_obj_obj_feats] = N1*max_obj_target + N2*max_skel_target +(i-(N1+N2))*max_obj_target*max_obj_target+j

            edges_obj_skel = mat(zeros((E2,2)))
            Ye2 = mat(zeros((max_obj_target*max_skel_target*E2,1)))
            for i in xrange(N1+N2+E1,N1+N2+E1+E2):
                target1 = int(input[i+1][0]);
                target2 = int(input[i+1][1]);
                if(target1 != -1 and target2 != -1): # both should be labeled to add to Ye
                #print target1 , target2
                    Ye2[(i-(N1+N2+E1))*max_obj_target*max_skel_target + (target1-1)*max_skel_target+(target2-1)]=1
                # get the segment numbers
                edges_obj_skel[i-(N1+N2+E1),0]= obj_map[int(input[i+1][2])]
                edges_obj_skel[i-(N1+N2+E1),1]= 0 #obj_map[int(input[i+1][3])]

                tokens = [line.split(':') for line in input[i+1][3:]]
                features = mat([float(v) for k,v in tokens])
            #print features
                f = features.transpose()

                # fill in the Xn matrix
                S = N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats + E1*max_obj_target*max_obj_target*num_obj_obj_feats
                for j in xrange(0,max_obj_target*max_skel_target):
                ##print X[j*9:(j+1)*9,j];
                #Xe[j*num_edge_feats:(j+1)*num_edge_feats,(i-N)*max_target*max_target+j] = f.copy();
                    xval[S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+j)*num_obj_skel_feats: S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+(j+1))*num_obj_skel_feats] = features.copy();
                    for v in xrange(0,num_obj_skel_feats):
                        xrow[S+((i-(N1+N2+E1))*max_obj_target*max_skel_target+j)*num_obj_skel_feats+v] = max_obj_target*num_obj_feats + max_skel_target*num_skel_feats + max_obj_target*max_obj_target*num_obj_obj_feats + j*num_obj_skel_feats+v
                    xcol[S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+j)*num_obj_skel_feats: S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+(j+1))*num_obj_skel_feats] = N1*max_obj_target + N2*max_skel_target + E1*max_obj_target*max_obj_target +(i-(N1+N2+E1))*max_obj_target*max_skel_target+j


            X_sparse = coo_matrix((xval,(xrow,xcol)),shape=(num_obj_feats*max_obj_target+ num_skel_feats*max_skel_target +num_obj_obj_feats*max_obj_target*max_obj_target+ num_obj_skel_feats*max_obj_target*max_skel_target,N1*max_obj_target+N2*max_skel_target+(E1*max_obj_target*max_obj_target)+(E2*max_obj_target*max_skel_target) ),dtype='d');

            Y = concatenate ((Yn,Ye1,Ye2))
            #xd =  X_sparse.todense()

            #numpy.savetxt('test.txt',xd,delimiter=' ',fmt='%-2.1f')
            edges_obj_obj_list.append(edges_obj_obj)
            edges_obj_skel_list.append(edges_obj_skel)
            N1_list.append(N1)
            E_list.append((E1,E2))
            obj_map_list.append(obj_map)
            frame_map[FN] = frame_count-1 # 0 indexed
            print frame_map
            #print FN, obj_map

            Y_s = csr_matrix(Y,dtype='d')
            K = max_target
           ## print frame_count

            if (frame_count ==1 ):
                X_multiple = X_sparse
                Y_multiple = Y
            else:

                data = scipy.concatenate((X_multiple.data, X_sparse.data))
                row= scipy.concatenate((X_multiple.row, X_sparse.row))
                col = scipy.concatenate((X_multiple.col, X_sparse.col + X_multiple.shape[1]))
                X_multiple = coo_matrix((data,(row,col)), shape= (X_multiple.shape[0], X_multiple.shape[1] + X_sparse.shape[1]) )
                Y_multiple = concatenate((Y_multiple, Y))
        #print obj_map_list
        if(TEMPORAL == "true"):
            temporal_edge_count = 0
            temporal_frames_list = []
            edges_obj_temporal_list = []
            for edge_num in xrange(1+int(files[0][0].strip()),1+int(files[0][0].strip())+int(files[0][1].strip())):
                edge_file = files[edge_num][0].strip()
                print edge_file
                temporal_edge_count += 1
                input = [line.split() for line in line_reader(file(edge_file.strip()))]
                # first line has the number of nodes and number of edges
                E3 = int(input[0][0].strip());
                E4 = int(input[0][1].strip());
                FN1 = int(input[0][2].strip());
                FN2 = int(input[0][3].strip());
                temporal_frames_list.append((frame_map[FN1],frame_map[FN2]))
                xrow = zeros( E3*max_obj_target*max_obj_target*num_obj_t_feats + E4*max_skel_target*max_skel_target*num_skel_t_feats)
                xcol = zeros( E3*max_obj_target*max_obj_target*num_obj_t_feats + E4*max_skel_target*max_skel_target*num_skel_t_feats)
                xval = zeros( E3*max_obj_target*max_obj_target*num_obj_t_feats + E4*max_skel_target*max_skel_target*num_skel_t_feats)
                #Xn= mat(zeros((max_target * num_node_feats,max_target*N)));
                Ye3 = mat(zeros((max_obj_target*max_obj_target*E3,1)))
                Ye4 = mat(zeros((max_skel_target*max_skel_target*E4,1)))
                edges_obj_temporal = mat(zeros((E3,1)))
                #edges_skel_temporal = mat(zeros((E4,1)))
                for i in xrange(0,E3):
                    target1 = int(input[i+1][0]);
                    target2 = int(input[i+1][1]);
                    if(target1 != -1 and target2 != -1): # both should be labeled to add to Ye
                        Ye3[i*max_obj_target*max_obj_target + (target1-1)*max_obj_target+(target2-1)]=1
                    # get the segment numbers
                    #print frame_map[FN2],obj_map_list[frame_map[FN2]]
                    edges_obj_temporal[i,0]= obj_map_list[frame_map[FN2]][int(input[i+1][2])]
                    

                    tokens = [line.split(':') for line in input[i+1][3:]]
                    features = mat([float(v) for k,v in tokens])
                    #print features
                    f = features.transpose()

                    # fill in the Xn matrix
                    for j in xrange(0,max_obj_target*max_obj_target):
                        xval[((i*max_obj_target*max_obj_target)+j)*num_obj_t_feats: (i*max_obj_target*max_obj_target+(j+1))*num_obj_t_feats] = features.copy();
                        for v in xrange(0,num_obj_t_feats):
                            xrow[(i*max_obj_target*max_obj_target+j)*num_obj_t_feats+v] =   j*num_obj_t_feats+v
                        xcol[ (i*max_obj_target*max_obj_target+j)*num_obj_t_feats:  (i*max_obj_target*max_obj_target+(j+1))*num_obj_t_feats] = i*max_obj_target*max_obj_target+j
                for i in xrange(E3,E3+E4):
                    target1 = int(input[i+1][0]);
                    target2 = int(input[i+1][1]);
                    if(target1 != -1 and target2 != -1): # both should be labeled to add to Ye
                        Ye4[(i-E3)*max_skel_target*max_skel_target + (target1-1)*max_skel_target+(target2-1)]=1
                    
                    #edges_skel_temporal[i-E3,0]= 1 # only one subactivity node

                    tokens = [line.split(':') for line in input[i+1][3:]]
                    features = mat([float(v) for k,v in tokens])
                    #print features
                    f = features.transpose()

                    # fill in the Xn matrix
                    S = E3*max_obj_target*max_obj_target*num_obj_t_feats
                    for j in xrange(0,max_skel_target*max_skel_target):
                        xval[S + (((i-E3)*max_skel_target*max_skel_target)+j)*num_skel_t_feats: S +((i-E3)*max_skel_target*max_skel_target+(j+1))*num_skel_t_feats] = features.copy();
                        for v in xrange(0,num_skel_t_feats):
                            xrow[S + ((i-E3)*max_skel_target*max_skel_target+j)*num_skel_t_feats+v] = max_obj_target*max_obj_target*num_obj_t_feats + j*num_skel_t_feats+v
                        xcol[ S+ ((i-E3)*max_skel_target*max_skel_target+j)*num_skel_t_feats:  S + ((i-E3)*max_skel_target*max_skel_target+(j+1))*num_skel_t_feats] =  E3*max_obj_target*max_obj_target + (i-E3)*max_skel_target*max_skel_target+j

                X_sparse = coo_matrix((xval,(xrow,xcol)),shape=(num_obj_t_feats*max_obj_target*max_obj_target+ num_skel_t_feats*max_skel_target*max_skel_target , E3*max_obj_target*max_obj_target +E4*max_skel_target*max_skel_target ),dtype='d');
                Y = concatenate ((Ye3,Ye4))
                #xd =  X_sparse.todense()

                #numpy.savetxt('test.txt',xd,delimiter=' ',fmt='%-2.1f')
                if (temporal_edge_count ==1 ):
                    X_temporal = X_sparse
                    Y_temporal = Y
                else:
                    data = scipy.concatenate((X_temporal.data, X_sparse.data))
                    row= scipy.concatenate((X_temporal.row, X_sparse.row))
                    col = scipy.concatenate((X_temporal.col, X_sparse.col + X_temporal.shape[1]))
                    X_temporal = coo_matrix((data,(row,col)), shape= (X_temporal.shape[0], X_temporal.shape[1] + X_sparse.shape[1]) )
                    Y_temporal = concatenate((Y_temporal, Y))

                edges_obj_temporal_list.append(edges_obj_temporal)
            #edges_skel_temporal_list.append(edges_skel_temporal)
            if (temporal_edge_count != 0):
                Y_multiple = concatenate((Y_multiple, Y_temporal))
                data = scipy.concatenate((X_multiple.data, X_temporal.data))
                row= scipy.concatenate((X_multiple.row, X_temporal.row + X_multiple.shape[0]))
                col = scipy.concatenate((X_multiple.col, X_temporal.col + X_multiple.shape[1]))
                X_multiple = coo_matrix((data,(row,col)), shape= ( X_multiple.shape[0] + X_temporal.shape[0], X_multiple.shape[1] + X_temporal.shape[1]) )
            else:
                data = X_multiple.data
                row= X_multiple.row
                col = X_multiple.col
                X_multiple = coo_matrix((data,(row,col)), shape= ( X_multiple.shape[0] + num_obj_t_feats*max_obj_target*max_obj_target+ num_skel_t_feats*max_skel_target*max_skel_target  , X_multiple.shape[1]) )


        Y_m_s = csr_matrix(Y_multiple,dtype='d');
        X_multiple = X_multiple.tocsr()
        #xd =  X_multiple.todense()
        #numpy.savetxt('matrixX.txt',xd,delimiter=' ',fmt='%-2.1f')
        #numpy.savetxt('matrixY.txt',Y_multiple,delimiter=' ',fmt='%-2.1f')
        print Y_m_s.shape
        print X_multiple.shape

        examples.append(((X_multiple, edges_obj_obj_list, edges_obj_skel_list, N1_list, E_list, frame_count, edges_obj_temporal_list, temporal_frames_list, temporal_edge_count,  example_num,obj_map_list ), (Y_m_s,N1_list,E_list,frame_count,temporal_edge_count,obj_map_list)))

    NUM_CLASSES = max_obj_target + max_skel_target

    # #print out some very useful statistics.
    print len(examples),'examples read'
    return examples

def read_examples_single_frame(filename,sparm):
    global NODEONLY
    global NUM_CLASSES
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL

    # Helper function for reading from files.
    def line_reader(lines):
        # returns only non-empty lines
        # strips comments (anything after '#')
        for l in lines:
            i = l.find('#')
            if i == -1: yield l.strip()


    """Parses an input file into an example sequence."""
    # This reads example files of the type read by SVM^multiclass.
    examples = []
    max_target=0
    num_obj_feats=0
    num_skel_feats=0
    num_obj_obj_feats=0
    num_obj_skel_feats=0


    start = time.clock()

    # Open the file and read each example.
    for input_file in file(filename):
        print input_file
        input = [line.split() for line in line_reader(file(input_file.strip()))]
        # first line has the number of nodes and number of edges
        N1 = int(input[0][0].strip())
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        E1 = int(input[0][1].strip())
        E2 = int(input[0][2].strip())
        K1 = int(input[0][3].strip())
        K2 = int(input[0][4].strip())

        # find the max class and number of node features -- will work for sparse representation
        for i in xrange(0,N1):
            tokens = [line.split(':') for line in input[i+1][2:]]
            for k,v in tokens:
                if(num_obj_feats<int(k)):
                    num_obj_feats=int(k)
        for i in xrange(N1, N1+N2):
            tokens = [line.split(':') for line in input[i+1][2:]]
            for k,v in tokens:
                if(num_skel_feats<int(k)):
                    num_skel_feats=int(k)
        for i in xrange(N1+N2, N1+N2+E1):
            tokens = [line.split(':') for line in input[i+1][4:]]
            for k,v in tokens:
                if(num_obj_obj_feats<int(k)):
                    num_obj_obj_feats=int(k)
        for i in xrange(N1+N2+E1,N1+N2+E1+E2):
            tokens = [line.split(':') for line in input[i+1][3:]]
            for k,v in tokens:
                if(num_obj_skel_feats<int(k)):
                    num_obj_skel_feats=int(k)
    max_obj_target = K1 # use the max number of classes read from the file
    max_skel_target = K2
    NUM_CLASSES_OBJ = K1
    NUM_CLASSES_SKEL = K2

    print 'number of obj classes: ', max_obj_target
    print 'number of skel classes: ', max_skel_target

    print 'number of obj features: ', num_obj_feats
    print 'number of skel features: ', num_skel_feats
    print 'number of obj obj edge features: ',num_obj_obj_feats
    print 'number of obj skel edge features: ',num_obj_skel_feats

    print 'time spent in preprocessing data files', start-time.clock()


    class_counts = zeros(K1+K2)

    example_num=-1
    for input_file in file(filename):
        print input_file
        example_num+=1
        input = [line.split() for line in line_reader(file(input_file.strip()))]
        # first line has the number of nodes and number of edges
        N1 = int(input[0][0].strip());
        N2 = 1
        E1 = int(input[0][1].strip());
        E2 = int(input[0][2].strip());
        xrow = zeros(N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats  + E1*max_obj_target*max_obj_target*num_obj_obj_feats + E2*max_obj_target*max_skel_target*num_obj_skel_feats )
        xcol = zeros(N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats  + E1*max_obj_target*max_obj_target*num_obj_obj_feats + E2*max_obj_target*max_skel_target*num_obj_skel_feats)
        xval = zeros(N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats  + E1*max_obj_target*max_obj_target*num_obj_obj_feats + E2*max_obj_target*max_skel_target*num_obj_skel_feats)
        #Xn= mat(zeros((max_target * num_node_feats,max_target*N)));
        Yn= mat(zeros((max_obj_target*N1+max_skel_target*N2,1)))

        #XY_test = mat(zeros((max_target*num_node_feats + max_target*max_target*num_edge_feats,1)))
        obj_map = {}

        for i in xrange(0,N1):
            target = int(input[i+1][0]);
            if(target != -1): # if the segment is unlabeled all entries of Yn for the label will be 0
                #print target
                class_counts[target-1]+=1
                Yn[i*max_obj_target+(target-1),0]=1

            # get the segment number
            obj_map[int(input[i+1][1])] = i

            # Get the features.
            tokens = [line.split(':') for line in input[i+1][2:]]

            # assumes all features are present
            features = mat([float(v) for k,v in tokens])
            #print features
            f = features.transpose()

            # fill in the Xn matrix
            for j in xrange(0,max_obj_target):
                xval[(i*max_obj_target+j)*num_obj_feats:(i*max_obj_target+j+1)*num_obj_feats] = features.A[0];
                for v in xrange(0,num_obj_feats):
                  xrow[(i*max_obj_target+j)*num_obj_feats+v] = j*num_obj_feats+v
                xcol[(i*max_obj_target+j)*num_obj_feats:(i*max_obj_target+j+1)*num_obj_feats] = i*max_obj_target+(j)
        #skel nodes
        for i in xrange(0, N2):
            target = int(input[N1+i+1][0]);
            
            if(target != -1): # if the segment is unlabeled all entries of Yn for the label will be 0
                Yn[N1*max_obj_target + i*max_skel_target+(target-1),0]=1
           
            # Get the features.
            tokens = [line.split(':') for line in input[N1+i+1][2:]]

            # assumes all features are present
            features = mat([float(v) for k,v in tokens])
            #print features
            f = features.transpose()

            # fill in the Xn matrix
            for j in xrange(0,max_skel_target):
                xval[N1*max_obj_target*num_obj_feats+(i*max_skel_target+j)*num_skel_feats:N1*max_obj_target*num_obj_feats+(i*max_skel_target+j+1)*num_skel_feats] = features.A[0];
                for v in xrange(0,num_skel_feats):
                  xrow[N1*max_obj_target*num_obj_feats+(i*max_skel_target+j)*num_skel_feats+v] = max_obj_target*num_obj_feats + j*num_skel_feats+v
                xcol[N1*max_obj_target*num_obj_feats + (i*max_skel_target+j)*num_skel_feats : N1*max_obj_target*num_obj_feats + (i*max_skel_target+j+1)*num_skel_feats] = N1*max_obj_target + i*max_skel_target+(j)
            ##print X
        #Xe = mat(zeros((max_target*max_target*num_edge_feats,max_target*max_target*E)))
        edges_obj_obj = mat(zeros((E1,2)))
        Ye1 = mat(zeros((max_obj_target*max_obj_target*E1,1)))
        for i in xrange(N1+N2,N1+N2+E1):
            target1 = int(input[i+1][0]);
            target2 = int(input[i+1][1]);
            if(target1 != -1 and target2 != -1): # both should be labeled to add to Ye
                Ye1[(i-(N1+N2))*max_obj_target*max_obj_target + (target1-1)*max_obj_target+(target2-1)]=1
            # get the segment numbers
            edges_obj_obj[i-(N1+N2),0]= obj_map[int(input[i+1][2])]
            edges_obj_obj[i-(N1+N2),1]= obj_map[int(input[i+1][3])]

            tokens = [line.split(':') for line in input[i+1][4:]]
            features = mat([float(v) for k,v in tokens])
            #print features
            f = features.transpose()
            #z = max_target*num_obj_feats + (target1-1)*max_target*num_edge_feats+(target2-1)*num_edge_feats
            #XY_test[z : z+num_edge_feats ,0] += f
            # fill in the Xn matrix
            S = N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats
            for j in xrange(0,max_obj_target*max_obj_target):
                ##print X[j*9:(j+1)*9,j];
                #Xe[j*num_edge_feats:(j+1)*num_edge_feats,(i-N)*max_target*max_target+j] = f.copy();
                xval[S + ((i-(N1+N2))*max_obj_target*max_obj_target+j)*num_obj_obj_feats: S + ((i-(N1+N2))*max_obj_target*max_obj_target+(j+1))*num_obj_obj_feats] = features.copy();
                for v in xrange(0,num_obj_obj_feats):
                  xrow[S+((i-(N1+N2))*max_obj_target*max_obj_target+j)*num_obj_obj_feats+v] = max_obj_target*num_obj_feats + max_skel_target*num_skel_feats + j*num_obj_obj_feats+v
                xcol[S + ((i-(N1+N2))*max_obj_target*max_obj_target+j)*num_obj_obj_feats: S + ((i-(N1+N2))*max_obj_target*max_obj_target+(j+1))*num_obj_obj_feats] = N1*max_obj_target + N2*max_skel_target +(i-(N1+N2))*max_obj_target*max_obj_target+j
        #print Xn.shape[0], num_node_feats*K
        #print Xn.shape[1] , N*K
        #print Xe.shape[0], num_edge_feats*K*K
        #print Xe.shape[1] , E*K*K
        #print xval
        #print xrow
        #print xcol
        edges_obj_skel = mat(zeros((E2,2)))
        Ye2 = mat(zeros((max_obj_target*max_skel_target*E2,1)))
        for i in xrange(N1+N2+E1,N1+N2+E1+E2):
            target1 = int(input[i+1][0]);
            target2 = int(input[i+1][1]);
            if(target1 != -1 and target2 != -1): # both should be labeled to add to Ye
                #print target1 , target2
                Ye2[(i-(N1+N2+E1))*max_obj_target*max_skel_target + (target1-1)*max_skel_target+(target2-1)]=1
            # get the segment numbers
            edges_obj_skel[i-(N1+N2+E1),0]= obj_map[int(input[i+1][2])]
            edges_obj_skel[i-(N1+N2+E1),1]= 0 #obj_map[int(input[i+1][3])]

            tokens = [line.split(':') for line in input[i+1][3:]]
            features = mat([float(v) for k,v in tokens])
            #print features
            f = features.transpose()
           # z = max_target*num_node_feats + (target1-1)*max_target*num_edge_feats+(target2-1)*num_edge_feats
            #XY_test[z : z+num_edge_feats ,0] += f
            # fill in the Xn matrix
            S = N1*max_obj_target*num_obj_feats + N2*max_skel_target*num_skel_feats + E1*max_obj_target*max_obj_target*num_obj_obj_feats
            for j in xrange(0,max_obj_target*max_skel_target):
                ##print X[j*9:(j+1)*9,j];
                #Xe[j*num_edge_feats:(j+1)*num_edge_feats,(i-N)*max_target*max_target+j] = f.copy();
                xval[S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+j)*num_obj_skel_feats: S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+(j+1))*num_obj_skel_feats] = features.copy();
                for v in xrange(0,num_obj_skel_feats):
                  xrow[S+((i-(N1+N2+E1))*max_obj_target*max_skel_target+j)*num_obj_skel_feats+v] = max_obj_target*num_obj_feats + max_skel_target*num_skel_feats + max_obj_target*max_obj_target*num_obj_obj_feats + j*num_obj_skel_feats+v
                xcol[S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+j)*num_obj_skel_feats: S + ((i-(N1+N2+E1))*max_obj_target*max_skel_target+(j+1))*num_obj_skel_feats] = N1*max_obj_target + N2*max_skel_target + E1*max_obj_target*max_obj_target +(i-(N1+N2+E1))*max_obj_target*max_skel_target+j


        X_sparse = csr_matrix((xval,(xrow,xcol)),shape=(num_obj_feats*max_obj_target+ num_skel_feats*max_skel_target +num_obj_obj_feats*max_obj_target*max_obj_target+ num_obj_skel_feats*max_obj_target*max_skel_target,N1*max_obj_target+N2*max_skel_target+(E1*max_obj_target*max_obj_target)+(E2*max_obj_target*max_skel_target) ),dtype='d');
        #a = concatenate ((Xn, mat(zeros((Xn.shape[0],Xe.shape[1])))),1)
        #b = concatenate ((mat(zeros((Xe.shape[0],Xn.shape[1]))),Xe),1)
        #X = concatenate ((a,b))
        Y = concatenate ((Yn,Ye1,Ye2))
        #print Y
        xd =  X_sparse.todense()

        numpy.savetxt('test.txt',xd,delimiter=' ',fmt='%-2.1f')
        #X_s = csr_matrix(X,dtype='d')
        #print sum(X_s.todense() - X_sparse.todense())
        #assert (sum(X_s.todense() - X_sparse.todense()) == 0)
        #assert ((X_s - X_sparse).sum() == 0)

        Y_s = csr_matrix(Y,dtype='d')
        K = max_target
        examples.append(((X_sparse, edges_obj_obj, edges_obj_skel, N1, E1 ,example_num, obj_map ), (Y_s,N1,E1,obj_map)))

    NUM_CLASSES = max_obj_target + max_skel_target

    # #print out some very useful statistics.
    print len(examples),'examples read'
    return examples
    

def get_index(edges,u,v):
    for i in xrange(0,edges.shape[0]):
        if (edges[i,0] == u and edges[i,1] == v):
            return i
    assert(2 == 1) # should never reach here

def init_model(sample, sm, sparm):

    """Store the number of features and classes in the model."""
    # Note that these features will be stored in the model and written
    # when it comes time to write the model to a file, and restored in
    # the classifier when reading the model from the file.
    ##print sample[0][0].shape[0]
    global NUM_CLASSES
    #sm.num_features = sample[0][0][0].shape[0]
    sm.num_features = sample[0][0][0].get_shape()[0]
    sm.num_classes = NUM_CLASSES
    print 'num of classes: ', sm.num_classes
    sm.size_psi = sm.num_features
    print 'size_psi set to: ',sm.size_psi

thecount = 0







def lp_inference_sum1_IP(X,sm,sparm,LE):
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
    start = time.clock()

    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    w = sm.w
    edges_obj_obj = X[1]
    edges_obj_skel = X[2]
    E1 = edges_obj_obj.shape[0]
    E2 = edges_obj_skel.shape[0]
    obj_map = X[6]
    N1 = X[3]
    N2 = 1
    if(NODEONLY == "true"):
        N2 =  0
    lp = glpk.LPX()        # Create empty problem instance
    lp.name = 'inference'     # Assign symbolic name to problem
    lp.obj.maximize = True # Set this as a maximization problem
    lp.cols.add(X[0].shape[1])         # Append three columns to this instance
    #lp.cols.add(X[0].get_shape()[1])         # Append three columns to this instance
    #count_t= 0
    for c in lp.cols:      # Iterate over all columns
        if (c.index < N1*K1):
            c.name = 'y_obj_%d_%d' % ( c.index/K1 , (c.index%K1)+1) # Name them y_obj_0_1, etc
            c.kind=int
            
        elif((c.index - N1*K1) < N2*K2) :
            index = c.index  - N1*K1
            c.name = 'y_skel_%d_%d' % ( index/K2 , (index%K2) + 1 ) # name them y_skel_0_1 etc
            c.kind = int
            
        elif((c.index - N1*K1 - N2*K2) < K1*K1*E1):
            index = c.index - N1*K1 - N2*K2
            c.name = 'y_%d-%d_%d-%d' % ( edges_obj_obj[int(index/(K1*K1)),0] ,edges_obj_obj[int(index/(K1*K1)),1] , int((index%(K1*K1))/K1)+1 , int((index%(K1*K1))%K1)+1)
            
        else :
            index = c.index - N1*K1 - N2*K2 - K1*K1*E1
            c.name = 'y_%d-%d_%d-%d' % ( edges_obj_skel[int(index/(K1*K2)),0] ,edges_obj_skel[int(index/(K1*K2)),1] , int((index%(K1*K2))/K2)+1 , int((index%(K1*K2))%K2)+1)
           
        c.bounds = 0.0, 1.0    # Set bound 0 <= xi <= 1
        #count_t +=1
    #print count_t,X[0].shape[1]
    x = X[0]
    #x = (X[0]).todense()
    w_list = [w[i] for i in xrange(0,x.shape[0])]
    w_mat = csr_matrix(asmatrix(array(w_list)),dtype='d')
    ##print w_list
    ##print (asarray(w*x)[0]).tolist()
    
    #print w_mat.transpose().shape[1];

    lp.obj[:] = (asarray((w_mat*x).todense())[0]).tolist() 
    ##print lp.obj[:]

    lp.rows.add(3*E1*K1*K1+3*E2*K1*K2+N1+N2)
    for r in lp.rows:      # Iterate over all rows
        r.name = 'p%d' %  r.index # Name them

    for i in xrange(0,2*E1*K1*K1):
        lp.rows[i].bounds = 0, None
    for i in xrange(2*E1*K1*K1,3*E1*K1*K1):
        lp.rows[i].bounds = None,1
    for i in xrange(3*E1*K1*K1,3*E1*K1*K1 +2*E2*K1*K2):
        lp.rows[i].bounds = 0, None
    for i in xrange(3*E1*K1*K1 + 2*E2*K1*K2, 3*E1*K1*K1 + 3*E2*K1*K2):
        lp.rows[i].bounds = None,1
    for i in xrange(3*E1*K1*K1 + 3*E2*K1*K2 ,3*E1*K1*K1 + 3*E2*K1*K2 + N1):
		if (LE == False) :
			lp.rows[i].bounds = 1,1  ##SUM = 1
		else:
			lp.rows[i].bounds = None,1  ## SUM = 1 is changed to SUM<= 1
    for i in xrange(3*E1*K1*K1 + 3*E2*K1*K2 +N1 ,3*E1*K1*K1 + 3*E2*K1*K2 + N1 + N2):
		if (LE == False) :
			lp.rows[i].bounds = 1,1  ##SUM = 1
		else:
			lp.rows[i].bounds = None,1  ## SUM = 1 is changed to SUM<= 1

    t = []
    for e in xrange(0,E1):
        u = edges_obj_obj[e,0]
        v = edges_obj_obj[e,1]
        n = -1
        for i in xrange(0,K1):
            for j in xrange(0,K1):
                n += 1
                a = int(u*K1 + i)
                b = int(v*K1 + j)
                c = N1*K1 + N2*K2 + e*K1*K1 + i*K1 + j
                ec = e*K1*K1 + n
                t.append((ec,a,1))
                t.append((ec,c,-1))
                ec += E1*K1*K1
                t.append((ec,b,1))
                t.append((ec,c,-1))
                ec += E1*K1*K1
                t.append((ec,a,1))
                t.append((ec,b,1))
                t.append((ec,c,-1))
    for e in xrange(0,E2):
        u = edges_obj_skel[e,0]
        v = edges_obj_skel[e,1]
        n = 3*E1*K1*K1 -1
        for i in xrange(0,K1):
            for j in xrange(0,K2):
                n += 1
                a = int(u*K1 + i)
                b = int(K1*N1+ v*K2 + j)
                c = N1*K1 + N2*K2 + E1*K1*K1 + e*K1*K2 + i*K2 + j
                ec = e*K1*K2 + n
                t.append((ec,a,1))
                t.append((ec,c,-1))
                ec += E2*K1*K2
                t.append((ec,b,1))
                t.append((ec,c,-1))
                ec += E2*K1*K2
                t.append((ec,a,1))
                t.append((ec,b,1))
                t.append((ec,c,-1))
    for e in xrange(0,N1):
        r = 3*E1*K1*K1 + 3*E2*K1*K2 +e
        for i in xrange(0,K1):
            c = e*K1+i
            t.append((r,c,1))
    for e in xrange(0,N2):
        r = 3*E1*K1*K1 + 3*E2*K1*K2 + N1 +e
        for i in xrange(0,K2):
            c = K1*N1+ e*K2+i
            t.append((r,c,1))
    

    ##print len(t)
    lp.matrix = t
    retval=lp.simplex();

    lpFin = time.clock()
    print "Time for LP:", (lpFin-start)

    assert retval == None
    labeling = asmatrix(array([c.primal for c in lp.cols]))
    for c in lp.cols:      # Iterate over all columns
        if (c.index < N1*K1 + N2*K2) :
            c.kind=int


    retval=lp.integer(tm_lim=300000)


    MIPFin = time.clock()
    print "Time for MIP:", (MIPFin-lpFin)

    assert retval == None or retval == "tmlim"
  #  #print 'Z = %g;' % lp.obj.value,  # Retrieve and #print obj func value
   # #print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                       # #print struct variable names and primal val
    if(retval == None):
        labeling = asmatrix(array([c.primal for c in lp.cols]))

    #print labeling.T
    #print labeling.shape
    ymax = (csr_matrix(labeling.T,dtype='d'),N1,E1,obj_map)
    #print ymax
    c1 = 0
    c0= 0
    ch =0
    cr = 0
    for c in lp.cols:
        if (c.primal == 1):
            c1 += 1
        elif(c.primal ==0):
            c0 += 1
        elif (c.primal == 0.5):
            ch += 1
        else:
            cr +=1
    #print 'number of 1s: %d' % c1
    #print 'number of 0s: %d' % c0
    #print 'number of 0.5s: %d' % ch
    #print 'number of 0s: %d' % cr
    #score = asarray((w_mat*x*ymax[0]).todense())[0][0];
    score2 = 0#sm.svm_model.classify(psi(x,ymax,sm,sparm))
    #print "objective value = ", round(lp.obj.value,2)
    #print '\n score : ' , round(score,2), ' score2: ',score2;
    #if(lp.obj.value  > 1.1):
    #  assert (round(lp.obj.value,2) ==  round(score,2))
    return ymax



def lp_training(X,Y,sm,sparm):
    global NODEONLY
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    N1 = X[3]
    N2 = 1
    if(NODEONLY == "true"):
        N2 =  0
    y = Y[0]
    w = sm.w
    edges_obj_obj = X[1]
    edges_obj_skel = X[2]

    E1 = edges_obj_obj.shape[0]
    E2 = edges_obj_skel.shape[0]
    lp = glpk.LPX()        # Create empty problem instance
    lp.name = 'training'     # Assign symbolic name to problem
    lp.obj.maximize = True # Set this as a maximization problem
    lp.cols.add(X[0].shape[1])         # Append three columns to this instance


    for c in lp.cols:      # Iterate over all columns
        if (c.index < N1*K1):
            c.name = 'y_obj_%d_%d' % ( c.index/K1 , (c.index%K1)+1) # Name them y_obj_0_1, etc
            c.kind=int
            
        elif((c.index - N1*K1) < N2*K2) :
            index = c.index  - N1*K1
            c.name = 'y_skel_%d_%d' % ( index/K2 , (index%K2) + 1 ) # name them y_skel_0_1 etc
            c.kind = int
            
        elif((c.index - N1*K1 - N2*K2) < K1*K1*E1):
            index = c.index - N1*K1 - N2*K2
            c.name = 'y_%d-%d_%d-%d' % ( edges_obj_obj[int(index/(K1*K1)),0] ,edges_obj_obj[int(index/(K1*K1)),1] , int((index%(K1*K1))/K1)+1 , int((index%(K1*K1))%K1)+1)
            
        else :
            index = c.index - N1*K1 - N2*K2 - K1*K1*E1
            c.name = 'y_%d-%d_%d-%d' % ( edges_obj_skel[int(index/(K1*K2)),0] ,edges_obj_skel[int(index/(K1*K2)),1] , int((index%(K1*K2))/K2)+1 , int((index%(K1*K2))%K2)+1)
            
        c.bounds = 0.0, 1.0    # Set bound 0 <= xi <= 1
        #count_t +=1
    #print count_t,X[0].shape[1]
    x = X[0]
    #x = (X[0]).todense()
    w_list = [w[i] for i in xrange(0,x.shape[0])]
    w_mat = csr_matrix(asmatrix(array(w_list)),dtype='d')
    ##print w_list
    ##print (asarray(w*x)[0]).tolist()
   
    #print w_mat.transpose().shape[1];

   # lp.obj[:] = (asarray((w_mat.transpose()*x).todense())[0]).tolist() ##!!!!!!!!!!!! why did this work without transpose before ?
    ##print lp.obj[:]



    coeff_list = (asarray((w_mat*x).todense())[0]).tolist()
    
    for index in xrange(0,N1*K1):
        if(y[index,0] == 1):
            coeff_list[index] = coeff_list[index]-(1.0/(N1*K1))
        else:
            coeff_list[index] = coeff_list[index]+(1.0/(N1*K1))
    for index in xrange( N1*K1, N1*K1 + N2*K2):
        if(y[index,0] == 1):
            coeff_list[index] = coeff_list[index]-(1.0/(N2*K2))
        else:
            coeff_list[index] = coeff_list[index]+(1.0/(N2*K2))

    lp.obj[:] = coeff_list

    lp.rows.add(3*E1*K1*K1+3*E2*K1*K2)
    for r in lp.rows:      # Iterate over all rows
        r.name = 'p%d' %  r.index # Name them

    for i in xrange(0,2*E1*K1*K1):
        lp.rows[i].bounds = 0, None
    for i in xrange(2*E1*K1*K1,3*E1*K1*K1):
        lp.rows[i].bounds = None,1
    for i in xrange(3*E1*K1*K1,3*E1*K1*K1 +2*E2*K1*K2):
        lp.rows[i].bounds = 0, None
    for i in xrange(3*E1*K1*K1 + 2*E2*K1*K2, 3*E1*K1*K1 + 3*E2*K1*K2):
        lp.rows[i].bounds = None,1


    t = []
    for e in xrange(0,E1):
        u = edges_obj_obj[e,0]
        v = edges_obj_obj[e,1]
        n = -1
        for i in xrange(0,K1):
            for j in xrange(0,K1):
                n += 1
                a = int(u*K1 + i)
                b = int(v*K1 + j)
                c = N1*K1 + N2*K2 + e*K1*K1 + i*K1 + j
                ec = e*K1*K1 + n
                t.append((ec,a,1))
                t.append((ec,c,-1))
                ec += E1*K1*K1
                t.append((ec,b,1))
                t.append((ec,c,-1))
                ec += E1*K1*K1
                t.append((ec,a,1))
                t.append((ec,b,1))
                t.append((ec,c,-1))
    for e in xrange(0,E2):
        u = edges_obj_skel[e,0]
        v = edges_obj_skel[e,1]
        n = 3*E1*K1*K1 -1
        for i in xrange(0,K1):
            for j in xrange(0,K2):
                n += 1
                a = int(u*K1 + i)
                b = int(K1*N1+ v*K2 + j)
                c = N1*K1 + N2*K2 + E1*K1*K1 + e*K1*K2 + i*K2 + j
                ec = e*K1*K2 + n
                t.append((ec,a,1))
                t.append((ec,c,-1))
                ec += E2*K1*K2
                t.append((ec,b,1))
                t.append((ec,c,-1))
                ec += E2*K1*K2
                t.append((ec,a,1))
                t.append((ec,b,1))
                t.append((ec,c,-1))




    ##print len(t)
    lp.matrix = t
    lp.simplex()
  #  #print 'Z = %g;' % lp.obj.value,  # Retrieve and #print obj func value
   # #print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                       # #print struct variable names and primal val
    labeling = asmatrix(array([c.primal for c in lp.cols]))
    ##print labeling.T.shape[0],labeling.T.shape[1]
    ymax = (csr_matrix(labeling.T,dtype='d'),N1,E1)
    
    c1 = 0
    c0= 0
    ch =0
    cr = 0
    for c in lp.cols:
        if (c.primal == 1):
            c1 += 1
        elif(c.primal ==0):
            c0 += 1
        elif (c.primal == 0.5):
            ch += 1
        else:
            cr +=1
    #print "LP Counts:"
    #print 'number of 1s: %d' % c1
    #print 'number of 0s: %d' % c0
    #print 'number of 0.5s: %d' % ch
    #print 'number of 0s: %d' % cr
   
    score = asarray((w_mat*x*ymax[0]).todense())[0][0];
    #print "score:" ,score
    #print "objective value= ", (lp.obj.value)
    #print "objective value w/ const= ", (lp.obj.value+(1.0/K1)+(1.0/K2))
    #print 'score w/ loss: ' , round(score+loss(Y,ymax,sparm),2) #, ' score2: ',score2;
    #print 'loss: ',loss(Y,ymax,sparm)
    #print '\n'
    if(lp.obj.value  > 2.1):
      assert (round(lp.obj.value+(1.0/K1)+(1.0/K2),2) ==  round(score+loss(Y,ymax,sparm),2))

    return ymax

def lp_training_temporal_qpbo(X,Y,sm,sparm):
    start = time.clock()

    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    num_frame = X[5]
    N1_list = X[3]
    E1_list = X[4]
    num_temporal_edges = X[8]
    temporal_frame_list =  X[7]
    w = sm.w
    y = Y[0]
    x = X[0]
    #x = (X[0]).todense()
    w_list = [w[i] for i in xrange(0,x.shape[0])]

    w_mat = csr_matrix(asmatrix(array(w_list)),dtype='d')
    ##print (asarray(w*x)[0]).tolist()

    coeff_list = (asarray((w_mat*x).todense())[0]).tolist()
   # print "coeff list length" , len(coeff_list)
    qpbo_edges = 0
    qpbo_nodes = 0
    for f_index in xrange(0,num_frame):
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        E1 = X[1][f_index].shape[0]
        E2 = X[2][f_index].shape[0]

        qpbo_edges += E1*K1*K1+E2*K1*K2
        qpbo_nodes += N1*K1+N2*K2

    for e_index in xrange(0, num_temporal_edges):
        #print e_index
        E3 = X[6][e_index].shape[0]
        E4 = 1
        if(NODEONLY == "true"):
            E4 =  0
        qpbo_edges += E3*K1*K1+E4*K2*K2

    #print qpbo_edges, qpbo_nodes, qpbo_nodes+qpbo_edges

    qpbo = QPBO(qpbo_nodes,qpbo_edges)        # Create empty problem instance
    qpbo.add_node(qpbo_nodes)
    index_jump = 0
    node_index_jump = 0
    index_jump_map = {}
    node_index_jump_map = {}
    for f_index in xrange(0,num_frame):
        index_jump_map[f_index] = index_jump
        node_index_jump_map[f_index] = node_index_jump
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        edges_obj_obj = X[1][f_index]
        edges_obj_skel = X[2][f_index]

        E1 = edges_obj_obj.shape[0]
        E2 = edges_obj_skel.shape[0]

        #print "N:",N," K: ", K

        for index_n in xrange(0,N1):
            for index_k in xrange(0,K1):
                if(y[index_jump + index_n*K1+index_k,0] == 1):
                    coeff_list[index_jump + index_n*K1+index_k] = coeff_list[index_jump + index_n*K1+index_k]-(1.0/(N1*K1))
                else:
                    coeff_list[index_jump + index_n*K1+index_k] = coeff_list[index_jump + index_n*K1+index_k]+(1.0/(N1*K1))
        for index_n in xrange(0,N2):
            for index_k in xrange(0,K2):
                if(y[index_jump + N1*K1+index_n*K2+index_k,0] == 1):
                    coeff_list[index_jump + N1*K1+index_n*K2+index_k] = coeff_list[index_jump + N1*K1+index_n*K2+index_k]-(1.0/(N2*K2))
                else:
                    coeff_list[index_jump + N1*K1+index_n*K2+index_k] = coeff_list[index_jump + N1*K1+index_n*K2+index_k]+(1.0/(N2*K2))

        for index in xrange(0,N1*K1+N2*K2):
            qpbo.add_term(index+node_index_jump,0,-coeff_list[index+index_jump]);

        for index in xrange(0,E1*K1*K1):
            u = edges_obj_obj[int(index/(K1*K1)),0]
            v = edges_obj_obj[int(index/(K1*K1)),1]
            l = int((index%(K1*K1))/K1)
            k = int((index%(K1*K1))%K1)

            n1 = int(u*K1 + l) + node_index_jump
            n2 = int(v*K1 + k) + node_index_jump
           # print index+N1*K1+N2*K2 + index_jump
            qpbo.add_term(n1,n2,0,0,0,-coeff_list[index+N1*K1+N2*K2 + index_jump])

        for index in xrange(0,E2*K1*K2):
            u = edges_obj_skel[int(index/(K1*K2)),0]
            v = edges_obj_skel[int(index/(K1*K2)),1]
            l = int((index%(K1*K2))/K2)
            k = int((index%(K1*K2))%K2)

            n1 = int(u*K1 + l) + node_index_jump
            n2 = int(N1*K1+ v*K2 + k) + node_index_jump
            qpbo.add_term(n1,n2,0,0,0,-coeff_list[index+N1*K1+N2*K2+E1*K1*K1 + index_jump])

        node_index_jump += N1*K1 + N2*K2
        index_jump += N1*K1+N2*K2+E1*K1*K1+E2*K1*K2

    for e_index in xrange(0, num_temporal_edges):
        edges_obj_temporal = X[6][e_index]
        F1 = temporal_frame_list[e_index][0]
        F2 = temporal_frame_list[e_index][1]
        E3 = X[6][e_index].shape[0]
        E4 = 1
        if(NODEONLY == "true"):
            E4 =  0
        for index in xrange(0,E3*K1*K1):
            u = edges_obj_temporal[int(index/(K1*K1)),0]
            
            l = int((index%(K1*K1))/K1)
            k = int((index%(K1*K1))%K1)

            n1 = int(u*K1 + l) + node_index_jump_map[F1]
            n2 = int(u*K1 + k) + node_index_jump_map[F2]
            qpbo.add_term(n1,n2,0,0,0,-coeff_list[index + index_jump])

        for index in xrange(0,E4*K2*K2):
            u = 0 # only one sub activity node
            
            l = int((index%(K2*K2))/K2)
            k = int((index%(K2*K2))%K2)

            n1 = int(N1*K1+ u*K2 + l) + node_index_jump_map[F1]
            n2 = int(N1*K1+ u*K2 + k) + node_index_jump_map[F2]
            qpbo.add_term(n1,n2,0,0,0,-coeff_list[index+E3*K1*K1 + index_jump])
        
        index_jump+= E3*K1*K1 + E4*K2*K2
        ##print lp.obj[:]
    qpbo.solve();
    qpbo.compute_weak_persistencies();

    labellist = [];
    node_index_jump = 0
    index_jump = 0
    for f_index in xrange(0,num_frame):
        ##print index_jump
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        edges_obj_obj = X[1][f_index]
        edges_obj_skel = X[2][f_index]

        E1 = edges_obj_obj.shape[0]
        E2 = edges_obj_skel.shape[0]

        for n in xrange(0,N1*K1+N2*K2):
            l = qpbo.get_label(n + node_index_jump);
            ##print n,l
            if(l == 0):
                labellist.append(0);
            elif(l ==1):
                labellist.append(1);
            else:
                labellist.append(0.5);

        for index in xrange(0,E1*K1*K1):
            u = edges_obj_obj[int(index/(K1*K1)),0]
            v = edges_obj_obj[int(index/(K1*K1)),1]
            l = int((index%(K1*K1))/K1)
            k = int((index%(K1*K1))%K1)

            l1 = labellist[int(u*K1 + l) + index_jump]
            l2 = labellist[int(v*K1 + k) + index_jump]
            if(l1*l2 == 0.25):
                if(coeff_list[index+N1*K1+N2*K2 + index_jump]>0):
                    labellist.append(0.5)
                else:
                    labellist.append(0)
            else:
                labellist.append(l1*l2);

        for index in xrange(0,E2*K1*K2):
            u = edges_obj_skel[int(index/(K1*K2)),0]
            v = edges_obj_skel[int(index/(K1*K2)),1]
            l = int((index%(K1*K2))/K2)
            k = int((index%(K1*K2))%K2)

            l1 = labellist[int(u*K1 + l) + index_jump]
            l2 = labellist[int(N1*K1+v*K2 + k) + index_jump]
            if(l1*l2 == 0.25):
                if(coeff_list[index+N1*K1+N2*K2+E1*K1*K1 + index_jump]>0):
                    labellist.append(0.5)
                else:
                    labellist.append(0)
            else:
                labellist.append(l1*l2);

        node_index_jump += N1*K1 + N2*K2
        index_jump += N1*K1+N2*K2+E1*K1*K1+E2*K1*K2

    for e_index in xrange(0, num_temporal_edges):
        edges_obj_temporal = X[6][e_index]
        F1 = temporal_frame_list[e_index][0]
        F2 = temporal_frame_list[e_index][1]
        E3 = X[6][e_index].shape[0]
        E4 = 1
        if(NODEONLY == "true"):
            E4 =  0
        for index in xrange(0,E3*K1*K1):
            u = edges_obj_temporal[int(index/(K1*K1)),0]

            l = int((index%(K1*K1))/K1)
            k = int((index%(K1*K1))%K1)

            l1 = labellist[int(u*K1 + l) + index_jump_map[F1]]
            l2 = labellist[int(u*K1 + k) + index_jump_map[F2]]
            if(l1*l2 == 0.25):
                if(coeff_list[index + index_jump]>0):
                    labellist.append(0.5)
                else:
                    labellist.append(0)
            else:
                labellist.append(l1*l2);

        for index in xrange(0,E4*K2*K2):
            u = 0 # only one subactivity node
            l = int((index%(K2*K2))/K2)
            k = int((index%(K2*K2))%K2)

            l1 = labellist[int(N1*K1+u*K2 + l) +  index_jump_map[F1]]
            l2 = labellist[int(N1*K1+u*K2 + k) +  index_jump_map[F2]]
            if(l1*l2 == 0.25):
                if(coeff_list[index+E3*K1*K1 + index_jump]>0):
                    labellist.append(0.5)
                else:
                    labellist.append(0)
            else:
                labellist.append(l1*l2);
        index_jump+= E3*K1*K1 + E4*K2*K2

  #  #print 'Z = %g;' % lp.obj.value,  # Retrieve and #print obj func value
   # #print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                       # #print struct variable names and primal val
    labeling = asmatrix(array([labellist]))
    #print labeling.T.shape[0],labeling.T.shape[1]
    ymax = (csr_matrix(labeling.T,dtype='d'),N1_list,E1_list, num_frame)
    c1 = 0
    c0= 0
    ch =0

    for c in labellist:
        if (c == 1):
            c1 += 1
        elif(c ==0):
            c0 += 1
        else:
            ch +=1
    #print "QPBO counts:"
    #print 'number of 1s: %d' % c1
    #print 'number of 0s: %d' % c0
    #print 'number of 0.5s: %d' % ch
    ##print ymax
    ##print ymax[0].todense().size, labeling.size,  len(labellist)
    score = asarray((w_mat*x*ymax[0]).todense())[0][0];

    #print "objective value w/ const= ", (lp.obj.value+(1.0/K))
    #print 'score : ' , round(score+loss(Y,ymax,sparm),2)
    #print 'loss: ',loss(Y,ymax,sparm)
    #print '\n'

    #assert (round(lp.obj.value+(1.0/K),2) ==  round(score+loss(Y,ymax,sparm),2))
    fin = time.clock()
  #  print "Time for qpbo:", (fin-start)
    return ymax

def lp_training_multiple_frames_qpbo(X,Y,sm,sparm):
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    num_frame = X[5]
    N1_list = X[3]
    E1_list = X[4]
    w = sm.w
    y = Y[0]
    x = X[0]
    #x = (X[0]).todense()
    w_list = [w[i] for i in xrange(0,x.shape[0])]

    w_mat = csr_matrix(asmatrix(array(w_list)),dtype='d')
    ##print (asarray(w*x)[0]).tolist()
    
    coeff_list = (asarray((w_mat*x).todense())[0]).tolist()
    
    qpbo_edges = 0
    qpbo_nodes = 0
    for f_index in xrange(0,num_frame):
        N1 = N1_list[f_index]
        N2 = 1

        E1 = X[1][f_index].shape[0]
        E2 = X[2][f_index].shape[0]

        qpbo_edges += E1*K1*K1+E2*K1*K2
        qpbo_nodes += N1*K1+N2*K2

    #print qpbo_edges, qpbo_nodes, qpbo_nodes+qpbo_edges

    qpbo = QPBO(qpbo_nodes,qpbo_edges)        # Create empty problem instance
    qpbo.add_node(qpbo_nodes)
    index_jump = 0
    node_index_jump = 0
    for f_index in xrange(0,num_frame):
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        edges_obj_obj = X[1][f_index]
        edges_obj_skel = X[2][f_index]

        E1 = edges_obj_obj.shape[0]
        E2 = edges_obj_skel.shape[0]

        #print "N:",N," K: ", K

        for index_n in xrange(0,N1):
            for index_k in xrange(0,K1):
                if(y[index_jump + index_n*K1+index_k,0] == 1):
                    coeff_list[index_jump + index_n*K1+index_k] = coeff_list[index_jump + index_n*K1+index_k]-(1.0/(N1*K1))
                else:
                    coeff_list[index_jump + index_n*K1+index_k] = coeff_list[index_jump + index_n*K1+index_k]+(1.0/(N1*K1))
        for index_n in xrange(0,N2):
            for index_k in xrange(0,K2):
                if(y[index_jump + N1*K1+index_n*K2+index_k,0] == 1):
                    coeff_list[index_jump + N1*K1+index_n*K2+index_k] = coeff_list[index_jump + N1*K1+index_n*K2+index_k]-(1.0/(N2*K2))
                else:
                    coeff_list[index_jump + N1*K1+index_n*K2+index_k] = coeff_list[index_jump + N1*K1+index_n*K2+index_k]+(1.0/(N2*K2))

        for index in xrange(0,N1*K1+N2*K2):
            qpbo.add_term(index+node_index_jump,0,-coeff_list[index+index_jump]);

        for index in xrange(0,E1*K1*K1):
            u = edges_obj_obj[int(index/(K1*K1)),0]
            v = edges_obj_obj[int(index/(K1*K1)),1]
            l = int((index%(K1*K1))/K1)
            k = int((index%(K1*K1))%K1)

            n1 = int(u*K1 + l) + node_index_jump
            n2 = int(v*K1 + k) + node_index_jump
            qpbo.add_term(n1,n2,0,0,0,-coeff_list[index+N1*K1+N2*K2 + index_jump])

        for index in xrange(0,E2*K1*K2):
            u = edges_obj_skel[int(index/(K1*K2)),0]
            v = edges_obj_skel[int(index/(K1*K2)),1]
            l = int((index%(K1*K2))/K2)
            k = int((index%(K1*K2))%K2)

            n1 = int(u*K1 + l) + node_index_jump
            n2 = int(N1*K1+ v*K2 + k) + node_index_jump
            qpbo.add_term(n1,n2,0,0,0,-coeff_list[index+N1*K1+N2*K2+E1*K1*K1 + index_jump])

        node_index_jump += N1*K1 + N2*K2
        index_jump += N1*K1+N2*K2+E1*K1*K1+E2*K1*K2
        ##print lp.obj[:]
    qpbo.solve();
    qpbo.compute_weak_persistencies();

    labellist = [];
    node_index_jump = 0
    index_jump = 0
    for f_index in xrange(0,num_frame):
        ##print index_jump
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0

        edges_obj_obj = X[1][f_index]
        edges_obj_skel = X[2][f_index]

        E1 = edges_obj_obj.shape[0]
        E2 = edges_obj_skel.shape[0]

        for n in xrange(0,N1*K1+N2*K2):
            l = qpbo.get_label(n + node_index_jump);
            ##print n,l
            if(l == 0):
                labellist.append(0);
            elif(l ==1):
                labellist.append(1);
            else:
                labellist.append(0.5);

        for index in xrange(0,E1*K1*K1):
            u = edges_obj_obj[int(index/(K1*K1)),0]
            v = edges_obj_obj[int(index/(K1*K1)),1]
            l = int((index%(K1*K1))/K1)
            k = int((index%(K1*K1))%K1)

            l1 = labellist[int(u*K1 + l) + index_jump]
            l2 = labellist[int(v*K1 + k) + index_jump]
            if(l1*l2 == 0.25):
                if(coeff_list[index+N1*K1+N2*K2 + index_jump]>0):
                    labellist.append(0.5)
                else:
                    labellist.append(0)
            else:
                labellist.append(l1*l2);

        for index in xrange(0,E2*K1*K2):
            u = edges_obj_skel[int(index/(K1*K2)),0]
            v = edges_obj_skel[int(index/(K1*K2)),1]
            l = int((index%(K1*K2))/K2)
            k = int((index%(K1*K2))%K2)

            l1 = labellist[int(u*K1 + l) + index_jump]
            l2 = labellist[int(N1*K1+v*K2 + k) + index_jump]
            if(l1*l2 == 0.25):
                if(coeff_list[index+N1*K1+N2*K2+E1*K1*K1 + index_jump]>0):
                    labellist.append(0.5)
                else:
                    labellist.append(0)
            else:
                labellist.append(l1*l2);

        node_index_jump += N1*K1 + N2*K2
        index_jump += N1*K1+N2*K2+E1*K1*K1+E2*K1*K2
  #  #print 'Z = %g;' % lp.obj.value,  # Retrieve and #print obj func value
   # #print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                       # #print struct variable names and primal val
    labeling = asmatrix(array([labellist]))
    #print labeling.T.shape[0],labeling.T.shape[1]
    ymax = (csr_matrix(labeling.T,dtype='d'),N1_list,E1_list, num_frame)
    c1 = 0
    c0= 0
    ch =0

    for c in labellist:
        if (c == 1):
            c1 += 1
        elif(c ==0):
            c0 += 1
        else:
            ch +=1
    #print "QPBO counts:"
    #print 'number of 1s: %d' % c1
    #print 'number of 0s: %d' % c0
    #print 'number of 0.5s: %d' % ch
    ##print ymax
    ##print ymax[0].todense().size, labeling.size,  len(labellist)
    score = asarray((w_mat*x*ymax[0]).todense())[0][0];

    #print "objective value w/ const= ", (lp.obj.value+(1.0/K))
    #print 'score : ' , round(score+loss(Y,ymax,sparm),2)
    #print 'loss: ',loss(Y,ymax,sparm)
    #print '\n'

    #assert (round(lp.obj.value+(1.0/K),2) ==  round(score+loss(Y,ymax,sparm),2))
    return ymax

def lp_inference_multiple_frames_sum1_IP(X,sm,sparm,LE):
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
    start = time.clock()

    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    num_frames = X[5]
    num_temporal_edges = X[8]
    obj_map_list = X[10]
    

  #  print X[3],X[4]

    w = sm.w
    
    x = X[0]
    N1_list = X[3]
    E1_list = X[4]
    #x = (X[0]).todense()

    w_list = [w[i] for i in xrange(0,x.shape[0])]
    ##print w_list

    w_mat = csr_matrix(asmatrix(array(w_list)),dtype='d')
    ##print w_mat.shape , x.shape
    lp = glpk.LPX()        # Create empty problem instance
    lp.name = 'inference'     # Assign symbolic name to problem
    lp.obj.maximize = True # Set this as a maximization problem
    lp.cols.add(X[0].shape[1])         # Append three columns to this instance
    lp.obj[:] = (asarray((w_mat*x).todense())[0]).tolist()
    ##print lp.obj[:]
    num_rows = 0
    for f_index in xrange(0,num_frames):
        E1 = X[1][f_index].shape[0]
        E2 = X[2][f_index].shape[0]
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        num_rows += 3*E1*K1*K1+3*E2*K1*K2+N1+N2

    lp.rows.add(num_rows)
    for r in lp.rows:      # Iterate over all rows
        r.name = 'p%d' %  r.index # Name them

    index_jump =0
    row_index_jump = 0
    t = []
    for f_index in xrange(0,num_frames):

        edges_obj_obj = X[1][f_index]
        edges_obj_skel = X[2][f_index]
        E1 = edges_obj_obj.shape[0]
        E2 = edges_obj_skel.shape[0]
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0

        #lp.cols.add(X[0].get_shape()[1])         # Append three columns to this instance
        #count_t= 0
        for c in lp.cols:      # Iterate over all columns
            if (c.index < index_jump + N1*K1):
                index = c.index  - index_jump
                c.name = 'y_obj_%d_%d_%d' % ( f_index, index/K1 , (index%K1)+1) # Name them y_obj_0_1, etc
                c.kind=int

            elif((c.index - index_jump - N1*K1) < N2*K2) :
                index = c.index  - index_jump - N1*K1
                c.name = 'y_skel_%d_%d_%d' % ( f_index, index/K2 , (index%K2) + 1 ) # name them y_skel_0_1 etc
                c.kind = int

            elif((c.index - index_jump - N1*K1 - N2*K2) < K1*K1*E1):
                index = c.index - index_jump - N1*K1 - N2*K2
                c.name = 'y_%d_%d-%d_%d-%d' % ( f_index, edges_obj_obj[int(index/(K1*K1)),0] ,edges_obj_obj[int(index/(K1*K1)),1] , int((index%(K1*K1))/K1)+1 , int((index%(K1*K1))%K1)+1)

            elif((c.index - index_jump - N1*K1 - N2*K2 - K1*K1*E1) < K1*K2*E2) :
                index = c.index - index_jump - N1*K1 - N2*K2 - K1*K1*E1
                ##print index, K1, K2, index_jump
                c.name = 'y_%d_%d-%d_%d-%d' % ( f_index, edges_obj_skel[int(index/(K1*K2)),0] ,edges_obj_skel[int(index/(K1*K2)),1] , int((index%(K1*K2))/K2)+1 , int((index%(K1*K2))%K2)+1)

            c.bounds = 0.0, 1.0    # Set bound 0 <= xi <= 1
       
        for i in xrange(row_index_jump, row_index_jump + 2*E1*K1*K1):
            lp.rows[i].bounds = 0, None
        for i in xrange(row_index_jump + 2*E1*K1*K1, row_index_jump + 3*E1*K1*K1):
            lp.rows[i].bounds = None,1
        for i in xrange(row_index_jump + 3*E1*K1*K1, row_index_jump + 3*E1*K1*K1 +2*E2*K1*K2):
            lp.rows[i].bounds = 0, None
        for i in xrange(row_index_jump + 3*E1*K1*K1 + 2*E2*K1*K2, row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2):
            lp.rows[i].bounds = None,1
        for i in xrange(row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 ,row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 + N1):
            if (LE == False) :
                lp.rows[i].bounds = 1,1  ##SUM = 1
            else:
                lp.rows[i].bounds = None,1  ## SUM = 1 is changed to SUM<= 1
        for i in xrange(row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 +N1 ,row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 + N1 + N2):
            if (LE == False) :
                lp.rows[i].bounds = 1,1  ##SUM = 1
            else:
                lp.rows[i].bounds = None,1  ## SUM = 1 is changed to SUM<= 1


        for e in xrange(0,E1):
            u = edges_obj_obj[e,0]
            v = edges_obj_obj[e,1]
            n = -1
            for i in xrange(0,K1):
                for j in xrange(0,K1):
                    n += 1
                    a = int(u*K1 + i) + index_jump
                    b = int(v*K1 + j) + index_jump
                    c = N1*K1 + N2*K2 + e*K1*K1 + i*K1 + j + index_jump
                    ec = e*K1*K1 + n + row_index_jump
                    t.append((ec,a,1))
                    t.append((ec,c,-1))
                    ec += E1*K1*K1
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
                    ec += E1*K1*K1
                    t.append((ec,a,1))
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
        for e in xrange(0,E2):
            u = edges_obj_skel[e,0]
            v = edges_obj_skel[e,1]
            n = 3*E1*K1*K1 -1
            for i in xrange(0,K1):
                for j in xrange(0,K2):
                    n += 1
                    a = int(u*K1 + i) + index_jump
                    b = int(K1*N1+ v*K2 + j) + index_jump
                    c = N1*K1 + N2*K2 + E1*K1*K1 + e*K1*K2 + i*K2 + j + index_jump
                    ec = e*K1*K2 + n + row_index_jump
                    t.append((ec,a,1))
                    t.append((ec,c,-1))
                    ec += E2*K1*K2
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
                    ec += E2*K1*K2
                    t.append((ec,a,1))
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
        for e in xrange(0,N1):
            r = 3*E1*K1*K1 + 3*E2*K1*K2 +e + row_index_jump
            for i in xrange(0,K1):
                c = e*K1+i + index_jump
                t.append((r,c,1))
        for e in xrange(0,N2):
            r = 3*E1*K1*K1 + 3*E2*K1*K2 + N1 +e + row_index_jump
            for i in xrange(0,K2):
                c = K1*N1+ e*K2+i + index_jump
                t.append((r,c,1))

        row_index_jump += 3*E1*K1*K1+3*E2*K1*K2+N1+N2
        index_jump += N1*K1 + N2*K2 + K1*K1*E1 + K1*K2*E2

    ##print len(t)
    ##print t
    lp.matrix = t
    retval=lp.simplex();

    lpFin = time.clock()
    print "Time for LP:", (lpFin-start)

    assert retval == None
    labeling = asmatrix(array([c.primal for c in lp.cols]))
    ##print labeling
    index_jump =0
    for f_index in xrange(0,num_frames):
        E1 = X[1][f_index].shape[0]
        E2 = X[2][f_index].shape[0]
        N1 = X[3][f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        for c in lp.cols:      # Iterate over all columns
            if (c.index - index_jump < N1*K1 + N2*K2 and c.index > index_jump) :
                c.kind=int
        index_jump += N1*K1 + N2*K2 + K1*K1*E1 + K1*K2*E2

    retval=lp.integer(tm_lim=300000)


    MIPFin = time.clock()
    print "Time for MIP:", (MIPFin-lpFin)

    assert retval == None or retval == "tmlim"
  #  #print 'Z = %g;' % lp.obj.value,  # Retrieve and #print obj func value
   # #print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                       # #print struct variable names and primal val
    if(retval == None):
        labeling = asmatrix(array([c.primal for c in lp.cols]))

    #print labeling.T
    #print labeling.shape
   # ymax = (csr_matrix(labeling.T,dtype='d'),N1_list,E1_list,num_frames)
    ymax = (csr_matrix(labeling.T,dtype='d'),N1_list,E1_list,num_frames,num_temporal_edges, obj_map_list)

    #print ymax
    c1 = 0
    c0= 0
    ch =0
    cr = 0
    for c in lp.cols:
        if (c.primal == 1):
            c1 += 1
        elif(c.primal ==0):
            c0 += 1
        elif (c.primal == 0.5):
            ch += 1
        else:
            cr +=1
    #print 'number of 1s: %d' % c1
    #print 'number of 0s: %d' % c0
    #print 'number of 0.5s: %d' % ch
    #print 'number of 0s: %d' % cr
    #score = asarray((w_mat*x*ymax[0]).todense())[0][0];
    score2 = 0#sm.svm_model.classify(psi(x,ymax,sm,sparm))
    #print "objective value = ", round(lp.obj.value,2)
    #print '\n score : ' , round(score,2), ' score2: ',score2;
    #if(lp.obj.value  > 1.1):
    #  assert (round(lp.obj.value,2) ==  round(score,2))
    return ymax

def lp_inference_temporal_sum1_IP(X,sm,sparm,LE):
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    start = time.clock()
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    num_frames = X[5]
    num_temporal_edges = X[8]
    obj_map_list = X[10]


   # print X[3],X[4]

    w = sm.w

    x = X[0]
    N1_list = X[3]
    E1_list = X[4]
    temporal_frame_list = X[7]

    #x = (X[0]).todense()

    w_list = [w[i] for i in xrange(0,x.shape[0])]
    ##print w_list

    w_mat = csr_matrix(asmatrix(array(w_list)),dtype='d')
    ##print w_mat.shape , x.shape
    lp = glpk.LPX()        # Create empty problem instance
    lp.name = 'inference'     # Assign symbolic name to problem
    lp.obj.maximize = True # Set this as a maximization problem
    lp.cols.add(X[0].shape[1])         # Append three columns to this instance
    lp.obj[:] = (asarray((w_mat*x).todense())[0]).tolist()
    ##print lp.obj[:]
    num_rows = 0
    for f_index in xrange(0,num_frames):
        E1 = X[1][f_index].shape[0]
        E2 = X[2][f_index].shape[0]
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        num_rows += 3*E1*K1*K1+3*E2*K1*K2+N1+N2

    for e_index in xrange(0, num_temporal_edges):
        E3 = X[6][e_index].shape[0]
        E4 = 1
        if(NODEONLY == "true"):
            E4 =  0
        num_rows += 3*E3*K1*K1+3*E4*K2*K2

    lp.rows.add(num_rows)
    for r in lp.rows:      # Iterate over all rows
        r.name = 'p%d' %  r.index # Name them

    index_jump =0
    row_index_jump = 0
    t = []
    index_jump_map = {}
    for f_index in xrange(0,num_frames):
        index_jump_map[f_index] = index_jump
        edges_obj_obj = X[1][f_index]
        edges_obj_skel = X[2][f_index]
        E1 = edges_obj_obj.shape[0]
        E2 = edges_obj_skel.shape[0]
        N1 = N1_list[f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0

        #lp.cols.add(X[0].get_shape()[1])         # Append three columns to this instance
        #count_t= 0
        for cnum in xrange(index_jump,index_jump + N1*K1):      # Iterate over all columns
            index = cnum  - index_jump
            lp.cols[cnum].name = 'y_obj_%d_%d_%d' % ( f_index, index/K1 , (index%K1)+1) # Name them y_obj_0_1, etc
            lp.cols[cnum].kind=int
            lp.cols[cnum].bounds = 0.0, 1.0
        for cnum in xrange(index_jump + N1*K1, index_jump + N1*K1 + N2*K2):
            index = cnum  - index_jump - N1*K1
            lp.cols[cnum].name = 'y_skel_%d_%d_%d' % ( f_index, index/K2 , (index%K2) + 1 ) # name them y_skel_0_1 etc
            lp.cols[cnum].kind = int
            lp.cols[cnum].bounds = 0.0, 1.0
        for cnum in xrange(index_jump + N1*K1 + N2*K2, index_jump + N1*K1 + N2*K2 + K1*K1*E1):
            index = cnum - index_jump - N1*K1 - N2*K2
            lp.cols[cnum].name = 'y_%d_%d-%d_%d-%d' % ( f_index, edges_obj_obj[int(index/(K1*K1)),0] ,edges_obj_obj[int(index/(K1*K1)),1] , int((index%(K1*K1))/K1)+1 , int((index%(K1*K1))%K1)+1)
            lp.cols[cnum].bounds = 0.0, 1.0
        for cnum in xrange(index_jump + N1*K1 + N2*K2 + K1*K1*E1, index_jump + N1*K1 + N2*K2 + K1*K1*E1 + K1*K2*E2) :
            index = cnum - index_jump - N1*K1 - N2*K2 - K1*K1*E1
            ##print index, K1, K2, index_jump
            lp.cols[cnum].name = 'y_%d_%d-%d_%d-%d' % ( f_index, edges_obj_skel[int(index/(K1*K2)),0] ,edges_obj_skel[int(index/(K1*K2)),1] , int((index%(K1*K2))/K2)+1 , int((index%(K1*K2))%K2)+1)
            lp.cols[cnum].bounds = 0.0, 1.0    # Set bound 0 <= xi <= 1

        for i in xrange(row_index_jump, row_index_jump + 2*E1*K1*K1):
            lp.rows[i].bounds = 0, None
        for i in xrange(row_index_jump + 2*E1*K1*K1, row_index_jump + 3*E1*K1*K1):
            lp.rows[i].bounds = None,1
        for i in xrange(row_index_jump + 3*E1*K1*K1, row_index_jump + 3*E1*K1*K1 +2*E2*K1*K2):
            lp.rows[i].bounds = 0, None
        for i in xrange(row_index_jump + 3*E1*K1*K1 + 2*E2*K1*K2, row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2):
            lp.rows[i].bounds = None,1
        for i in xrange(row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 ,row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 + N1):
            if (LE == False) :
                lp.rows[i].bounds = 1,1  ##SUM = 1
            else:
                lp.rows[i].bounds = None,1  ## SUM = 1 is changed to SUM<= 1
        for i in xrange(row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 +N1 ,row_index_jump + 3*E1*K1*K1 + 3*E2*K1*K2 + N1 + N2):
            if (LE == False) :
                lp.rows[i].bounds = 1,1  ##SUM = 1
            else:
                lp.rows[i].bounds = None,1  ## SUM = 1 is changed to SUM<= 1


        for e in xrange(0,E1):
            u = edges_obj_obj[e,0]
            v = edges_obj_obj[e,1]
            n = -1
            for i in xrange(0,K1):
                for j in xrange(0,K1):
                    n += 1
                    a = int(u*K1 + i) + index_jump
                    b = int(v*K1 + j) + index_jump
                    c = N1*K1 + N2*K2 + e*K1*K1 + i*K1 + j + index_jump
                    ec = e*K1*K1 + n + row_index_jump
                    t.append((ec,a,1))
                    t.append((ec,c,-1))
                    ec += E1*K1*K1
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
                    ec += E1*K1*K1
                    t.append((ec,a,1))
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
        for e in xrange(0,E2):
            u = edges_obj_skel[e,0]
            v = edges_obj_skel[e,1]
            n = 3*E1*K1*K1 -1
            for i in xrange(0,K1):
                for j in xrange(0,K2):
                    n += 1
                    a = int(u*K1 + i) + index_jump
                    b = int(K1*N1+ v*K2 + j) + index_jump
                    c = N1*K1 + N2*K2 + E1*K1*K1 + e*K1*K2 + i*K2 + j + index_jump
                    ec = e*K1*K2 + n + row_index_jump
                    t.append((ec,a,1))
                    t.append((ec,c,-1))
                    ec += E2*K1*K2
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
                    ec += E2*K1*K2
                    t.append((ec,a,1))
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
        for e in xrange(0,N1):
            r = 3*E1*K1*K1 + 3*E2*K1*K2 +e + row_index_jump
            for i in xrange(0,K1):
                c = e*K1+i + index_jump
                t.append((r,c,1))
        for e in xrange(0,N2):
            r = 3*E1*K1*K1 + 3*E2*K1*K2 + N1 +e + row_index_jump
            for i in xrange(0,K2):
                c = K1*N1+ e*K2+i + index_jump
                t.append((r,c,1))

        row_index_jump += 3*E1*K1*K1+3*E2*K1*K2+N1+N2
        index_jump += N1*K1 + N2*K2 + K1*K1*E1 + K1*K2*E2

    for e_index in xrange(0, num_temporal_edges):
        edges_obj_temporal = X[6][e_index]
        E3 = edges_obj_temporal.shape[0]
        E4 = 1
        if(NODEONLY == "true"):
            E4 =  0
        for cnum in xrange(index_jump, index_jump +  K1*K1*E3):
            index = cnum - index_jump
            lp.cols[cnum].name = 'y_t_o_%d_%d_%d-%d' % ( e_index, edges_obj_temporal[int(index/(K1*K1)),0] , int((index%(K1*K1))/K1)+1 , int((index%(K1*K1))%K1)+1)
            lp.cols[cnum].bounds = 0.0, 1.0
        for cnum in xrange(index_jump +  K1*K1*E3, index_jump + K1*K1*E3 + K2*K2*E4) :
            index = cnum - index_jump - N1*K1 - N2*K2 - K1*K1*E1
            ##print index, K1, K2, index_jump
            lp.cols[cnum].name = 'y_t_s_%d_%d-%d' % ( e_index, int((index%(K2*K2))/K2)+1 , int((index%(K2*K2))%K2)+1)
            lp.cols[cnum].bounds = 0.0, 1.0    # Set bound 0 <= xi <= 1


        for i in xrange(row_index_jump, row_index_jump + 2*E3*K1*K1):
            lp.rows[i].bounds = 0, None
        for i in xrange(row_index_jump + 2*E3*K1*K1, row_index_jump + 3*E3*K1*K1):
            lp.rows[i].bounds = None,1
        for i in xrange(row_index_jump + 3*E3*K1*K1, row_index_jump + 3*E3*K1*K1 +2*E4*K2*K2):
            lp.rows[i].bounds = 0, None
        for i in xrange(row_index_jump + 3*E3*K1*K1 + 2*E4*K2*K2, row_index_jump + 3*E3*K1*K1 + 3*E4*K2*K2):
            lp.rows[i].bounds = None,1

        for e in xrange(0,E3):
            u = edges_obj_temporal[e,0]
            index_jump_u = index_jump_map[temporal_frame_list[e_index][0]]
            index_jump_v = index_jump_map[temporal_frame_list[e_index][1]]
            n = -1
            for i in xrange(0,K1):
                for j in xrange(0,K1):
                    n += 1
                    a = int(u*K1 + i) + index_jump_u
                    b = int(u*K1 + j) + index_jump_v
                    c = e*K1*K1 + i*K1 + j + index_jump
                    ec = e*K1*K1 + n + row_index_jump
                    t.append((ec,a,1))
                    t.append((ec,c,-1))
                    ec += E3*K1*K1
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
                    ec += E3*K1*K1
                    t.append((ec,a,1))
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
        for e in xrange(0,E4):
            u = 0 # only one sub activity node
            index_jump_u = index_jump_map[temporal_frame_list[e_index][0]]
            index_jump_v = index_jump_map[temporal_frame_list[e_index][1]]
            n = 3*E3*K1*K1 -1
            for i in xrange(0,K2):
                for j in xrange(0,K2):
                    n += 1
                    a = int(K1*N1+ u*K2 + i) + index_jump_u
                    b = int(K1*N1+ u*K2 + j) + index_jump_v
                    c =  E3*K1*K1 + e*K2*K2 + i*K2 + j + index_jump
                    ec = e*K2*K2 + n + row_index_jump
                    t.append((ec,a,1))
                    t.append((ec,c,-1))
                    ec += E4*K2*K2
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
                    ec += E4*K2*K2
                    t.append((ec,a,1))
                    t.append((ec,b,1))
                    t.append((ec,c,-1))
        row_index_jump += 3*E3*K1*K1 + 3*E4*K2*K2
        index_jump += K1*K1*E3 + K2*K2*E4
    ##print len(t)
    ##print t
    lp.matrix = t
    retval=lp.simplex();

    lpFin = time.clock()
    print "Time for LP:", (lpFin-start)

    assert retval == None
    labeling = asmatrix(array([c.primal for c in lp.cols]))
    ##print labeling
    index_jump =0
    for f_index in xrange(0,num_frames):
        E1 = X[1][f_index].shape[0]
        E2 = X[2][f_index].shape[0]
        N1 = X[3][f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        for c in lp.cols:      # Iterate over all columns
            if (c.index - index_jump < N1*K1 + N2*K2 and c.index > index_jump) :
                c.kind=int
        index_jump += N1*K1 + N2*K2 + K1*K1*E1 + K1*K2*E2

    retval=lp.integer(tm_lim=300000)


    MIPFin = time.clock()
    print "Time for MIP:", (MIPFin-lpFin)

    assert retval == None or retval == "tmlim"
  #  #print 'Z = %g;' % lp.obj.value,  # Retrieve and #print obj func value
   # #print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                       # #print struct variable names and primal val
    if(retval == None):
        labeling = asmatrix(array([c.primal for c in lp.cols]))

    #print labeling.T
    #print labeling.shape
    ymax = (csr_matrix(labeling.T,dtype='d'),N1_list,E1_list,num_frames,num_temporal_edges, obj_map_list)
    #print ymax
    c1 = 0
    c0= 0
    ch =0
    cr = 0
    for c in lp.cols:
        if (c.primal == 1):
            c1 += 1
        elif(c.primal ==0):
            c0 += 1
        elif (c.primal == 0.5):
            ch += 1
        else:
            cr +=1
    #print 'number of 1s: %d' % c1
    #print 'number of 0s: %d' % c0
    #print 'number of 0.5s: %d' % ch
    #print 'number of 0s: %d' % cr
    #score = asarray((w_mat*x*ymax[0]).todense())[0][0];
    score2 = 0#sm.svm_model.classify(psi(x,ymax,sm,sparm))
    #print "objective value = ", round(lp.obj.value,2)
    #print '\n score : ' , round(score,2), ' score2: ',score2;
    #if(lp.obj.value  > 1.1):
    #  assert (round(lp.obj.value,2) ==  round(score,2))
    return ymax



def lp_training_qpbo(X,Y,sm,sparm):
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    N1 = X[3]
    N2 = 1
    if(NODEONLY == "true"):
        N2 =  0
    y = Y[0]
    w = sm.w
    edges_obj_obj = X[1]
    edges_obj_skel = X[2]

    E1 = edges_obj_obj.shape[0]
    E2 = edges_obj_skel.shape[0]

    qpbo = QPBO(N1*K1+N2*K2,E1*K1*K1+E2*K1*K2)        # Create empty problem instance
    qpbo.add_node(N1*K1+N2*K2)
    #print "N:",N," K: ", K
    x = X[0]
    #x = (X[0]).todense()
    w_list = [w[i] for i in xrange(0,x.shape[0])]

    w_mat = csr_matrix(asmatrix(array(w_list)),dtype='d')
    #print w_list
    ##print (asarray(w*x)[0]).tolist()
    coeff_list = (asarray((w_mat*x).todense())[0]).tolist()
    for index_n in xrange(0,N1):
        for index_k in xrange(0,K1):
            if(y[index_n*K1+index_k,0] == 1):
                coeff_list[index_n*K1+index_k] = coeff_list[index_n*K1+index_k]-(1.0/(N1*K1))
            else:
                coeff_list[index_n*K1+index_k] = coeff_list[index_n*K1+index_k]+(1.0/(N1*K1))
    for index_n in xrange(0,N2):
        
        for index_k in xrange(0,K2):
            if(y[N1*K1+index_n*K2+index_k,0] == 1):
                coeff_list[N1*K1+index_n*K2+index_k] = coeff_list[N1*K1+index_n*K2+index_k]-(1.0/(N2*K2))
            else:
                coeff_list[N1*K1+index_n*K2+index_k] = coeff_list[N1*K1+index_n*K2+index_k]+(1.0/(N2*K2))

    for index in xrange(0,N1*K1+N2*K2):
        qpbo.add_term(index,0,-coeff_list[index]);

    for index in xrange(0,E1*K1*K1):
        u = edges_obj_obj[int(index/(K1*K1)),0]
        v = edges_obj_obj[int(index/(K1*K1)),1]
        l = int((index%(K1*K1))/K1)
        k = int((index%(K1*K1))%K1)

        n1 = int(u*K1 + l)
        n2 = int(v*K1 + k)
        qpbo.add_term(n1,n2,0,0,0,-coeff_list[index+N1*K1+N2*K2])

    for index in xrange(0,E2*K1*K2):
        u = edges_obj_skel[int(index/(K1*K2)),0]
        v = edges_obj_skel[int(index/(K1*K2)),1]
        l = int((index%(K1*K2))/K2)
        k = int((index%(K1*K2))%K2)

        n1 = int(u*K1 + l)
        n2 = int(N1*K1+ v*K2 + k)
        qpbo.add_term(n1,n2,0,0,0,-coeff_list[index+N1*K1+N2*K2+E1*K1*K1])
    ##print lp.obj[:]
    qpbo.solve();
    qpbo.compute_weak_persistencies();

    labellist = [];
    for n in xrange(0,N1*K1+N2*K2):
        l = qpbo.get_label(n);
        #print n,l
        if(l == 0):
            labellist.append(0);
        elif(l ==1):
            labellist.append(1);
        else:
            labellist.append(0.5);

    for index in xrange(0,E1*K1*K1):
        u = edges_obj_obj[int(index/(K1*K1)),0]
        v = edges_obj_obj[int(index/(K1*K1)),1]
        l = int((index%(K1*K1))/K1)
        k = int((index%(K1*K1))%K1)

        l1 = labellist[int(u*K1 + l)]
        l2 = labellist[int(v*K1 + k)]
        if(l1*l2 == 0.25):
            if(coeff_list[index+N1*K1+N2*K2]>0):
                labellist.append(0.5)
            else:
                labellist.append(0)
        else:
            labellist.append(l1*l2);
    for index in xrange(0,E2*K1*K2):
        u = edges_obj_skel[int(index/(K1*K2)),0]
        v = edges_obj_skel[int(index/(K1*K2)),1]
        l = int((index%(K1*K2))/K2)
        k = int((index%(K1*K2))%K2)

        l1 = labellist[int(u*K1 + l)]
        l2 = labellist[int(N1*K1+v*K2 + k)]
        if(l1*l2 == 0.25):
            if(coeff_list[index+N1*K1+N2*K2+E1*K1*K1]>0):
                labellist.append(0.5)
            else:
                labellist.append(0)
        else:
            labellist.append(l1*l2);
  #  #print 'Z = %g;' % lp.obj.value,  # Retrieve and #print obj func value
   # #print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
                       # #print struct variable names and primal val
    labeling = asmatrix(array([labellist]))
    #print labeling.T.shape[0],labeling.T.shape[1]
    ymax = (csr_matrix(labeling.T,dtype='d'),N1,E1)
    c1 = 0
    c0= 0
    ch =0
    
    for c in labellist:
        if (c == 1):
            c1 += 1
        elif(c ==0):
            c0 += 1
        else:
            ch +=1
    #print "QPBO counts:"
    #print 'number of 1s: %d' % c1
    #print 'number of 0s: %d' % c0
    #print 'number of 0.5s: %d' % ch
    
    score = asarray((w_mat*x*ymax[0]).todense())[0][0];

    #print "objective value w/ const= ", (lp.obj.value+(1.0/K))
    #print 'score : ' , round(score+loss(Y,ymax,sparm),2)
    #print 'loss: ',loss(Y,ymax,sparm)
    #print '\n'
    
    #assert (round(lp.obj.value+(1.0/K),2) ==  round(score+loss(Y,ymax,sparm),2))
    return ymax



def classification_score(x,y,sm,sparm):
    """Return an example, label pair discriminant score."""
    # Utilize the svmapi.Model convenience method 'classify'.
    score = sm.svm_model.classify(psi(x,y,sm,sparm))
    global thecount
    thecount += 1
    if (sum(abs(w) for w in sm.w)):
        import pdb; pdb.set_trace()
    return score

def classify_example(x, sm, sparm):
    """Returns the classification of an example 'x'."""
    global SINGLE_FRAME
    global TEMPORAL
    #y = (mat(ones((1,x[0].shape[1]))),x[2],sm.num_classes)
    #l = lp_inference(x,sm,sparm)
    if(SINGLE_FRAME == "true"):
        l = lp_inference_sum1_IP(x,sm,sparm,False)
    elif(TEMPORAL == "false"):
        l = lp_inference_multiple_frames_sum1_IP(x, sm, sparm, False)
    else:
        l = lp_inference_temporal_sum1_IP(x, sm, sparm, False)
   
    return l

def areEqualVectors(V1,V2):
    for i in xrange(0,V1.shape[0]):
        assert(round(V1[i,0]*2, 0)==round(V2[i,0]*2, 0))
        
def find_most_violated_constraint(x, y, sm, sparm):
    """Returns the most violated constraint for example (x,y)."""
    # Similar, but include the loss.
    global SINGLE_FRAME
    global TEMPORAL
    #print "MOST VIOLATED Constraint"
    if( SINGLE_FRAME == "true"):
        l1 = lp_training_qpbo(x,y,sm,sparm)
    elif(TEMPORAL == "false" ):
        l1 = lp_training_multiple_frames_qpbo(x, y, sm, sparm)
    else:
        l1 = lp_training_temporal_qpbo(x, y, sm, sparm)
    #l1 = lp_training(x,y,sm,sparm)
    
    return l1

def psi(x, y, sm, sparm):
    
    """Returns the combined feature vector Psi(x,y)."""
    # Return the product of x and y

    #start = time.clock()
    b = coo_matrix(x[0]*y[0])
    #fin = time.clock()
    #print "Time for matrix multiplication:", (fin-start)

    c = [(b.row[i],b.data[i]) for i in xrange(0,len(b.row))]
    #fin1 = time.clock()
    #print "Time for todense:", (fin1-fin)
    #a = svmapi.Sparse((b.todense()))
    a = svmapi.Sparse((c))
    #fin2 = time.clock()
    #print "Time for psi:", (fin2-fin1)
    return a
    
def loss(Y, Ybar, sparm):
    #global LOSS_METHOD
    global SINGLE_FRAME
    if (SINGLE_FRAME == "true"):
        return loss_micro(Y, Ybar, sparm);
    else:
        return loss_multiple_frame_micro(Y, Ybar, sparm)

def loss_micro(Y, Ybar, sparm):
    """Loss is 1 if the labels are different, 0 if they are the same."""
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    N2 = 1
    if(NODEONLY == "true"):
        N2 =  0
    N1 = Y[1]
    E1 = Y[2]
    y= Y[0]
    
    #print "N:",N," K: ", K #,y.shape[0],y.shape[1]
    ybar = Ybar[0]
    
    yDiff=y- ybar;
    sum=0.0;
    size=N1*K1 + N2*K2
    

    for index_n in xrange(0,N1):
        for index_k in xrange(0,K1):
            if (y[index_n*K1 : index_n*K1+K1,0].sum() == 1):
                #print 'diff:', yDiff[index_n*K1+index_k,0]
                if yDiff[index_n*K1+index_k,0]>0:
                    sum+=yDiff[index_n*K1+index_k,0]/(N1*K1)
                else:
                    sum-=yDiff[index_n*K1+index_k,0]/(N1*K1)
                #print "sum:", sum
    #print "------"
    #print y
    #print N1*K1, N2*K2
    for index_n in xrange(0,N2):
        for index_k in xrange(0,K2):
            if (y[ N1*K1+ index_n*K2 : N1*K1 + index_n*K2+K2,0].sum() == 1):
                #print 'diff:', yDiff[index_n*K1+index_k,0]
                if yDiff[N1*K1 + index_n*K2+index_k,0]>0:
                    sum+=yDiff[N1*K1 + index_n*K2+index_k,0]/(N2*K2)
                else:
                    sum-=yDiff[ N1*K1 + index_n*K2+index_k,0]/(N2*K2)
                #print "sum:", sum
    #print sum
    return sum;

def loss_multiple_frame_micro(Y, Ybar, sparm):
    """Loss is 1 if the labels are different, 0 if they are the same."""
    global NUM_CLASSES_OBJ
    global NUM_CLASSES_SKEL
    global NODEONLY
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    N2 = 1
    if(NODEONLY == "true"):
        N2 =  0
    N1_list = Y[1]
    E_list = Y[2]
    num_frames = Y[3]
    y= Y[0]

    #print "N:",N," K: ", K #,y.shape[0],y.shape[1]
    ybar = Ybar[0]

    yDiff=y- ybar;
    sum=0.0;
    index_jump = 0

    for f_index in xrange(0,num_frames):
        N1 = N1_list[f_index]
        E1 = E_list[f_index][0]
        E2 = E_list[f_index][1]

        for index_n in xrange(0,N1):
            for index_k in xrange(0,K1):
                if (y[ index_jump + index_n*K1 : index_jump + index_n*K1+K1,0].sum() == 1):
                    #print 'diff:', yDiff[index_n*K1+index_k,0]
                    if yDiff[index_jump + index_n*K1+index_k,0]>0:
                        sum+=yDiff[index_jump + index_n*K1+index_k,0]/(N1*K1)
                    else:
                        sum-=yDiff[index_jump + index_n*K1+index_k,0]/(N1*K1)
                #print "sum:", sum
        #print "------"
        #print y
        #print N1*K1, N2*K2
        for index_n in xrange(0,N2):
            for index_k in xrange(0,K2):
                if (y[ index_jump + N1*K1+ index_n*K2 : index_jump + N1*K1 + index_n*K2+K2,0].sum() == 1):
                    #print 'diff:', yDiff[index_n*K1+index_k,0]
                    if yDiff[index_jump + N1*K1 + index_n*K2+index_k,0]>0:
                        sum+=yDiff[index_jump + N1*K1 + index_n*K2+index_k,0]/(N2*K2)
                    else:
                        sum-=yDiff[ index_jump + N1*K1 + index_n*K2+index_k,0]/(N2*K2)
                    #print "sum:", sum
        index_jump += N1*K1 + N2*K2 + E1*K1*K1 + E2*K1*K2
    #print sum
    return sum;

def write_label(fileptr, y):
    global SINGLE_FRAME
    global NUM_CLASSES_SKEL
    global NUM_CLASSES_OBJ
    global NODEONLY
    if(SINGLE_FRAME == "true"):
        K1 = NUM_CLASSES_OBJ
        K2 = NUM_CLASSES_SKEL
        #K= y[2]
        N1 = y[1]
        N2 = 1
        obj_map = y[3]
        #for node in xrange(0,N):
        #    for label in xrange(0,K):
         #       if(y[0][node*K+label,0] != 0):
         #           s = repr(node+1)+':'+repr(label+1)+':'+repr(y[0][node*K+label,0])
         #           print>>fileptr,s,
        #print>>fileptr
        if(N1>0):
           y_obj = y[0][0 : N1*NUM_CLASSES_OBJ]
        if(N2>0):
           y_skel = y[0][N1*NUM_CLASSES_OBJ:  N1*NUM_CLASSES_OBJ+N2*NUM_CLASSES_SKEL]
        s = ""
        for node in xrange(0,N1):
                maxscore = 0
                maxlabelList =[]
                for label in xrange(0,K1):
                    if(y_obj[node*K1+label,0] > maxscore):
                        maxscore = y_obj[node*K1+label,0]
                for label in xrange(0,K1):
                    if(y_obj[node*K1+label,0] == maxscore):
                        maxlabelList.append(label)
                maxlabel = maxlabelList[random.randint(0,len(maxlabelList))]
                objId =  [k for k, v in obj_map.iteritems() if v == node][0]
                s += repr(objId)+':'+repr(maxlabel+1)+':'+repr(maxscore)
                s += ","
        for node in xrange(0,N2):
                maxscore = 0
                maxlabelList = []
                for label in xrange(0,K2):
                    if(y_skel[node*K2+label,0] >maxscore):
                        maxscore = y_skel[node*K2+label,0]
                for label in xrange(0,K2):
                    if(y_skel[node*K2+label,0] == maxscore):
                        maxlabelList.append(label)
                maxlabel =  maxlabelList[random.randint(0,len(maxlabelList))]
                s += repr(node+1)+':'+repr(maxlabel+1)+':'+repr(maxscore)

        s+=";"
        print>>fileptr,s,
        print>>fileptr
    else:
        num_frames = y[3]
        obj_map_list = y[5]
        K1 = NUM_CLASSES_OBJ
        K2 = NUM_CLASSES_SKEL
        #per segment/frame print the objectid:object label; actid:actlabel
        index_jump =0
        s= ""
        for f_index in xrange(0,num_frames):

            N1 = y[1][f_index]
            N2 = 1
            if(NODEONLY == "true"):
                N2 =  0
            E1 = y[2][f_index][0]
            E2 = y[2][f_index][1]
            if(N1>0):
                y_obj = y[0][index_jump : index_jump + N1*NUM_CLASSES_OBJ]
            if(N2>0):
                y_skel = y[0][index_jump + N1*NUM_CLASSES_OBJ: index_jump + N1*NUM_CLASSES_OBJ+N2*NUM_CLASSES_SKEL]
            for node in xrange(0,N1):
                maxscore = 0
                maxlabelList =[]
                for label in xrange(0,K1):
                    if(y_obj[node*K1+label,0] > maxscore):
                        maxscore = y_obj[node*K1+label,0]
                for label in xrange(0,K1):
                    if(y_obj[node*K1+label,0] == maxscore):
                        maxlabelList.append(label)
                maxlabel = maxlabelList[random.randint(0,len(maxlabelList))]
                objId =  [k for k, v in obj_map_list[f_index].iteritems() if v == node][0]
                s += repr(objId)+':'+repr(maxlabel+1)+':'+repr(maxscore)
                s += ","
            for node in xrange(0,N2):
                maxscore = 0
                maxlabelList = []
                for label in xrange(0,K2):
                    if(y_skel[node*K2+label,0] >maxscore):
                        maxscore = y_skel[node*K2+label,0]
                for label in xrange(0,K2):
                    if(y_skel[node*K2+label,0] == maxscore):
                        maxlabelList.append(label)
                maxlabel =  maxlabelList[random.randint(0,len(maxlabelList))]
                s += repr(node+1)+':'+repr(maxlabel+1)+':'+repr(maxscore)
                        
            s+=";"
            index_jump += N1*K1+N2*K2+ E1*K1*K1 + E2*K1*K2
        print>>fileptr,s,
        print>>fileptr


def print_iteration_stats(ceps, cached_constraint, sample, sm,
                          cset, alpha, sparm):
    """Called just before the end of each cutting plane iteration.

    This is called just before the end of each cutting plane
    iteration, primarily to #print statistics.  The 'ceps' argument is
    how much the most violated constraint was violated by.  The
    'cached_constraint' argument is true if this constraint was
    constructed from the cache.
    
    The default behavior is that nothing is #printed."""
    # for every 10th iteration save the model file 
    global ITER
    ITER += 1;
    if(ITER%100 == 0):
        filename = "imodels/model.c"+ `sparm.c`  + ".m" + `ITER`;
        print "writing intermediate model: ", filename
        write_model(filename, sm, sparm)
    # #printig the weight vector
    #w_list = [sm.w[i] for i in xrange(0,sm.size_psi)]
    ##print w_list

def write_model(filename, sm, sparm):
    import cPickle, bz2
    cPickle.dump(sm,file(filename,'w'))

def read_model(filename, sparm):
    import cPickle, bz2
    return cPickle.load(file(filename))




def evaluation_class_pr_sum1(Y,Ybar,K,N,sparm):
    y = Y
    ybar = Ybar
    truecount = zeros((K,1))
    predcount = zeros((K,1))
    singlepredcount = zeros((K,1))
    tpcount = zeros((K,1))
    confusionMatrix=zeros((K,K))
    confusionMatrixWMultiple=zeros((K,K))
    multipleClasses=zeros((K,1))
    zeroClasses=zeros((K,1))
    prec = zeros((K,1))
    recall = zeros((K,1))
    f = open('pred.txt','a')
    print y,ybar
    for node in xrange(0,N):
        flag = 0;
        numPositives=0;
        predClass=-1;
        actualClass=-1;
        maxYBar=-1;
        countMax=0
        for label in xrange(0,K):
            print node,label
            if(y[node*K+label,0] == 1):
                truecount[label,0] += 1;
                actualClass=label
            if(maxYBar<ybar[node*K+label,0]):
                maxYBar=ybar[node*K+label,0]
                countMax=0
            if(maxYBar==ybar[node*K+label,0]):
                countMax+=1
        if(actualClass == -1):
            continue;
        maxLabelList=[];
        for label in xrange(0,K):
            if(ybar[node*K+label,0] == maxYBar and maxYBar>0): #suboptimal way, but who cares!
                maxLabelList.append(label);
                predcount[label,0] += 1;
                numPositives+=1;
                predClass=label;
                confusionMatrixWMultiple[label,actualClass]+=1.0/countMax;

        if(numPositives==0):
            zeroClasses[actualClass,0]+=1
        elif(numPositives>=1):
#            multipleClasses[actualClass,0]+=1
#        else:
            if(numPositives>1):
                prediction=maxLabelList[random.randint(0,countMax)]
            else:
                prediction=maxLabelList[0]
            confusionMatrix[prediction,actualClass]+=1
            singlepredcount[prediction,0] += 1;
            if(actualClass==prediction):
                tpcount[prediction,0] += 1
                flag = 1;
				
        print>>f, node+1,flag         
    print>>f, "\n"
    for label in xrange(0,K):
        if(singlepredcount[label,0] != 0):
            prec[label,0] = tpcount[label,0]/float(singlepredcount[label,0])
        if(truecount[label,0] !=0):
            recall[label,0] = tpcount[label,0]/float(truecount[label,0])
    return (tpcount,truecount,predcount,confusionMatrix,zeroClasses,multipleClasses,confusionMatrixWMultiple,singlepredcount)

def evaluation_prec_recall(Y, Ybar, K, N ,sparm):
    y = Y[0]
    ybar = Ybar[0]
    prec = 0.0
    recall = 0.0
    for node in xrange(0,N):
        tp_fn = 0.0
        tp_fp = 0.0
        tp= 0.0 #multiply(y[node*K:node*K+K],ybar[node*K:node*K+K])
        for label in xrange(0,K):
            tp_fn += y[node*K+label,0]*y[node*K+label,0]
            tp_fp += ybar[node*K+label,0]*ybar[node*K+label,0]
            tp += y[node*K+label,0]*ybar[node*K+label,0]
        
        if( tp_fp > 0):
            prec += tp/tp_fp; 
        else:
            prec += 0;
        if( tp_fn > 0):
            recall += tp/tp_fn; 
        else:
            recall += 0;

    ##print "similarity is", sim/N
    return (prec/N, recall/N);





def eval_prediction(exnum, (x, y), ypred, sm, sparm, teststats):
    """Accumulate statistics about a single training example.

    Allows accumulated statistics regarding how well the predicted
    label ypred for pattern x matches the true label y.  The first
    time this function is called teststats is None.  This function's
    return value will be passed along to the next call to
    eval_prediction.  After all test predictions are made, the last
    value returned will be passed along to #print_testing_stats.

    On the first call, that is, when exnum==0, teststats==None.  The
    default behavior is that the function does nothing."""
    global SINGLE_FRAME
    
    if exnum==0: teststats = []
    
    if(SINGLE_FRAME == "true"):
        teststats = eval_prediction_single_frame(exnum, (x, y), ypred, sm, sparm, teststats)
    else:
        teststats= eval_prediction_multi_frame(exnum, (x, y), ypred, sm, sparm, teststats)
    return teststats

def eval_prediction_single_frame(exnum, (x, y), ypred, sm, sparm, teststats):
    global NUM_CLASSES_SKEL
    global NUM_CLASSES_OBJ
    global NODEONLY
    if exnum==0: teststats = []

    N1 = y[1]
    N2 = 1
    if(NODEONLY == "true"):
        N2 =  0
    y_obj = y[0][0:N1*NUM_CLASSES_OBJ]
    y_skel = y[0][N1*NUM_CLASSES_OBJ:N1*NUM_CLASSES_OBJ+N2*NUM_CLASSES_SKEL]

    ypred_obj = ypred[0][0:N1*NUM_CLASSES_OBJ]
    ypred_skel = ypred[0][N1*NUM_CLASSES_OBJ:N1*NUM_CLASSES_OBJ+N2*NUM_CLASSES_SKEL]
    
    obj_res = evaluation_class_pr_sum1(y_obj, ypred_obj, NUM_CLASSES_OBJ , N1, sparm)
    skel_res = evaluation_class_pr_sum1(y_skel, ypred_skel, NUM_CLASSES_SKEL , N2, sparm)
    teststats.append((obj_res,skel_res))
    return teststats


def eval_prediction_multi_frame(exnum, (x, y), ypred, sm, sparm, teststats):
    global NUM_CLASSES_SKEL
    global NUM_CLASSES_OBJ
    global NODEONLY
    if exnum==0: teststats = []
    num_frames = y[3]
    K1 = NUM_CLASSES_OBJ
    K2 = NUM_CLASSES_SKEL
    index_jump =0
    for f_index in xrange(0,num_frames):
        
        N1 = y[1][f_index]
        N2 = 1
        if(NODEONLY == "true"):
            N2 =  0
        E1 = y[2][f_index][0]
        E2 =y[2][f_index][1]
        if(N1>0):
            y_obj = y[0][index_jump : index_jump + N1*NUM_CLASSES_OBJ]
        if(N2>0):
            y_skel = y[0][index_jump + N1*NUM_CLASSES_OBJ: index_jump + N1*NUM_CLASSES_OBJ+N2*NUM_CLASSES_SKEL]
        if(N1>0):
            ypred_obj = ypred[0][index_jump : index_jump + N1*NUM_CLASSES_OBJ]
        if(N2>0):
            ypred_skel = ypred[0][index_jump + N1*NUM_CLASSES_OBJ: index_jump + N1*NUM_CLASSES_OBJ+N2*NUM_CLASSES_SKEL]
        obj_res = []
        skel_res = []
        if(N1>0):
            obj_res = evaluation_class_pr_sum1(y_obj, ypred_obj, NUM_CLASSES_OBJ , N1, sparm)
        if(N2>0):
            skel_res = evaluation_class_pr_sum1(y_skel, ypred_skel, NUM_CLASSES_SKEL , N2, sparm)
        teststats.append((obj_res,skel_res))
        index_jump += N1*K1+N2*K2+ E1*K1*K1 + E2*K1*K2
    return teststats

def print_testing_stats_objects( K, teststats):

    avgp = zeros((K,1))
    avgr = zeros((K,1))
    tpcount = zeros((K,1))
    truecount = zeros((K,1))
    predcount = zeros((K,1))
    singlepredcount = zeros((K,1))
    aggConfusionMatrix=zeros((K,K),dtype='i')
    aggConfusionMatrixWMultiple=zeros((K,K),dtype='i')
    aggZeroPreds=zeros((K,1))
    aggMultiplePreds=zeros((K,1))
    for t in teststats:
        if (len(t) == 0):
            return
        tpcount += t[0]
        truecount += t[1]
        predcount += t[2]
        singlepredcount += t[7]
        aggConfusionMatrix+=t[3];
        aggZeroPreds +=t[4];
        aggMultiplePreds +=t[5];
        aggConfusionMatrixWMultiple+=t[6];


    total_tc  = 0
    total_pc = 0
    total_tp = 0
    for label in xrange(0,K):
        if(singlepredcount[label,0] != 0):
            avgp[label,0] = tpcount[label,0]/float(singlepredcount[label,0])
        if(truecount[label,0] !=0):
            avgr[label,0] = tpcount[label,0]/float(truecount[label,0])
      #  avgp[label,0] = avgp[label,0]/len(teststats)
      #  avgr[label,0] = avgr[label,0]/len(teststats)
        print "label ",label+1, " prec: " , avgp[label,0], " recall: " ,avgr[label,0], " tp: ", tpcount[label,0], " tc: ", truecount[label,0], " pc: ", singlepredcount[label,0]
        total_tc +=  truecount[label,0]
        total_pc += singlepredcount[label,0]
        total_tp += tpcount[label,0]
    print "prec: ", total_tp/total_pc , "recall: ",total_tp/total_tc ,"tp: ", total_tp, " pc: ", total_pc, "tc: ", total_tc
    #print "Error per Test example: ", teststats
    print "confusion matrix:"
    print aggConfusionMatrix;
    savetxt('conf.txt',aggConfusionMatrix,fmt='%d');

    print "confusion matrix with multiple semantics:"
    print aggConfusionMatrixWMultiple;
    savetxt('confm.txt',aggConfusionMatrixWMultiple,fmt='%d');

    print "num Zeros:"
    print aggZeroPreds;

    print "num Multiples:"
    print aggMultiplePreds;


def print_testing_stats(sample, sm, sparm, teststats):
    """#print statistics once classification has finished.

    This is called after all test predictions are made to allow the
    display of any summary statistics that have been accumulated in
    the teststats object through use of the eval_prediction function.

    The default behavior is that nothing is #printed."""

    teststats_obj = [a[0] for a in teststats]
    teststats_skel = [a[1] for a in teststats]
    if(len(teststats_obj[0])>0):
        print "Object detection : "
        print_testing_stats_objects(NUM_CLASSES_OBJ,teststats_obj )
    print "Activity detection : "
    print_testing_stats_objects(NUM_CLASSES_SKEL, teststats_skel)

