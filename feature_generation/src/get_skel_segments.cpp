#include <pcl/io/pcd_io.h>
#include "constants.h"

#include "readData.cpp"
#include "segmentation_skel.cpp"
#include <iostream>
#include <fstream>


std::ofstream segmentfile;
string dataLocation;
map<string, string> data_act_map;
map<string, vector<string> > data_obj_map;

void errorMsg(string message) {
    cout << "ERROR! " << message << endl;
    exit(1);
}

void parseChk(bool chk) {
    if (!chk) {
        errorMsg("parsing error.");
    }
}

void readDataActMap() {
    const string mapfile = dataLocation + "activityLabel.txt";

    printf("Opening map of data to activity: \"%s\"\n", (char*) mapfile.c_str());
    ifstream file((char*) mapfile.c_str(), ifstream::in);

    string line;
    int count = 0;
    while (getline(file, line)) {
        stringstream lineStream(line);
        string element1, element2, element3;
        parseChk(getline(lineStream, element1, ','));

        if (element1.compare("END") == 0) {
            break;
        }
        parseChk(getline(lineStream, element2, ','));
        if (element1.length() != 10) {
            errorMsg("Data Act Map file format mismatch..");
        }

        data_act_map[element1] = element2;
        parseChk(getline(lineStream, element3, ',')); // get actor
        while (getline(lineStream, element3, ',')) {
            data_obj_map[element1].push_back(element3);
        }



        cout << "\t" << element1 << " -> \"" << data_act_map[element1] << "\"" << endl;
        count++;
    }
    file.close();

    if (count == 0) {
        errorMsg("File does not exist or is empty!\n");
    }
    printf("\tcount = %d\n\n", count);
}

int
main(int argc, char **argv) {
    srand(time(0));

    //pcl::PointCloud<Point> cloud;

    // pcl::PCDReader pcd;
    // if (pcd.read (argv[1], cloud) == -1)
    //   return (-1);
    int method = atoi(argv[2]);
    float threshold = atof(argv[3]);
    dataLocation = argv[1];
    readDataActMap();
    vector<string> all_files;
    map<string, string>::iterator it = data_act_map.begin();
    while (it != data_act_map.end()) {
        all_files.push_back(it->first);
        it++;
    }
    
    double **data; //[JOINT_NUM][JOINT_DATA_NUM];
    int **data_CONF; //[JOINT_NUM][JOINT_DATA_TYPE_NUM]
    double **pos_data; //[POS_JOINT_NUM][POS_JOINT_DATA_NUM];
    int *pos_data_CONF; //[POS_JOINT_NUM]
    data = new double*[JOINT_NUM];
    data_CONF = new int*[JOINT_NUM];
    for (int i = 0; i < JOINT_NUM; i++) {
        data[i] = new double[JOINT_DATA_NUM];
        data_CONF[i] = new int[JOINT_DATA_TYPE_NUM];
    }
    pos_data = new double*[POS_JOINT_NUM];
    pos_data_CONF = new int[POS_JOINT_NUM];
    for (int i = 0; i < POS_JOINT_NUM; i++) {
        pos_data[i] = new double[POS_JOINT_DATA_NUM];
    }

    int ***IMAGE; // [X_RES][Y_RES]
    IMAGE = new int**[X_RES];
    for (int i = 0; i < X_RES; i++) {
        IMAGE[i] = new int*[Y_RES];
        for (int j = 0; j < Y_RES; j++) {
            IMAGE[i][j] = new int[RGBD_data];
        }
    }

    segmentfile.open("Segmentation.txt",ios::app);
    for (size_t i = 0; i < all_files.size(); i++) {
        int count = 1;

        //readData* DATA = new readData("/opt/ros/diamondback/stacks/object_affordance_detection/data/withaudio/hema-pouring/", "0925121318");
        readData* DATA = new readData(dataLocation, all_files.at(i));
        Segmentation_skel segSkel;

        int status = 1;
        string transformfile = dataLocation+ all_files.at(i) + "_globalTransform.bag";
        do {
            status = DATA->readNextFrame(data, pos_data, data_CONF, pos_data_CONF);
            if (status != 0)
                segSkel.addSkelFrame(data, pos_data, transformfile);
            cout << "status = " << status << endl;
        } while (status > 0);

        //segSkel.computeSegments();
        
        segSkel.computeSegmentsDynamic(threshold,method);
        segmentfile << all_files.at(i) << ";";
        segSkel.printSegments(segmentfile);

    }
    segmentfile.close();
}
    /** 
    there are 11 joints that have both orientation (3x3) and position (x,y,z) data
            XN_SKEL_HEAD,0
            XN_SKEL_NECK,1
            XN_SKEL_TORSO,2
            XN_SKEL_LEFT_SHOULDER,3
            XN_SKEL_LEFT_ELBOW,4
            XN_SKEL_RIGHT_SHOULDER,5
            XN_SKEL_RIGHT_ELBOW,6
            XN_SKEL_LEFT_HIP,7
            XN_SKEL_LEFT_KNEE,8
            XN_SKEL_RIGHT_HIP,9
            XN_SKEL_RIGHT_KNEE,10
	
    there are 4 joints that have only position (x,y,z) data
            XN_SKEL_LEFT_HAND,11
            XN_SKEL_RIGHT_HAND,12
            XN_SKEL_LEFT_FOOT,13
            XN_SKEL_RIGHT_FOOT,14

     data[][0~8]    -> orientation (3x3 matrix)
                         3x3 matrix is stored as 
                            0 1 2
                            3 4 5
                            6 7 8
                         read PDF for description about 3x3 matrix 
     data[][9~11]   -> x,y,z position for eleven joints
 
     data_CONF[][0]   -> confidence value of orientation  (data[][0~8]) 
     data_CONF[][1]   -> confidence value of xyz position (data[][9~11])
 
     data_pos[][0~2] -> x,y,z position for four joints
     data_pos_CONF[]  -> confidence value of xyz position (data_pos[][0~2])
 
    X_RES and Y_RES are in constants.h, so just use them.
     IMAGE[X_RES][Y_RES][0~2]   -> RGB values
     IMAGE[X_RES][Y_RES][3]     -> depth values

 
     */
