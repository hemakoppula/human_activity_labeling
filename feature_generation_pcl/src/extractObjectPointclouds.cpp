/* 
 * File:   featureGeneration.cpp
 * Author: hema
 *
 * Created on August 29, 2011, 6:16 PM
 */

#include <cstdlib>
#include <cstdio>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <cmath>
#include <dirent.h>
#include "constants.h"
//#include <opencv/cv.h>
//#include <opencv/highgui.h>

//#include "Point2D.h"
//#include "HOGFeaturesOfBlock.h"
//#include "HOG.h"
#include <pcl/point_types.h>
typedef pcl::PointXYZRGB PointT;
#include "includes/point_types.h"
#include "includes/CombineUtils.h"

#include "readData.cpp"

//#include "features.cpp"
//#include "featuresRGBD_skel.cpp"
//#include "features_singleFrame.cpp"
//#include "frame.cpp"
#include "includes/color.cpp"
//#include "pointcloudClustering.h"
#include "frame.cpp"

using namespace std;


int Frame::FrameNum = 0;
bool USE_HOG = false;

bool useHead = true;
bool useTorso = true;
bool useLeftArm = true;
bool useRightArm = true;
bool useLeftHand = true;
bool useRightHand = true;
bool useFullBody = true;
bool useImage = true;
bool useDepth = true;
bool useSkeleton = true;



map<string, string> data_act_map;
map<string, vector<string> > data_obj_map;
map<string, vector<string> > data_obj_type_map;
map<string, set<int> > FrameList;
string dataLocation;
string actfile;

// print error message

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
    const string mapfile = dataLocation + actfile;

    printf("Opening map of data to activity: \"%s\"\n",
            (char*) mapfile.c_str());
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
                        cout << element3 << endl;
            //vector<string> fields;
            //boost::split_regex( fields, element3, boost::regex( ":" ) );
                        int v = element3.find(":",0);
            cout << element3.substr(0,v) << endl;
            cout << element3.substr(v+1) << endl;

            data_obj_map[element1].push_back(element3.substr(0,v));

            data_obj_type_map[element1].push_back(element3.substr(v+1));
        }

        cout << "\t" << element1 << " : " << data_act_map[element1] << endl;
        count++;
    }
    file.close();

    if (count == 0) {
        errorMsg("File does not exist or is empty!\n");
    }
    printf("\tcount = %d\n\n", count);
}



// read file that maps data and activity

void readDataActMapOld() {
    const string mapfile = dataLocation + actfile;

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



void saveTablePC( pcl::PointCloud<PointT> &cloud, pcl::PointIndices &tablePointInds  ){
  if(tablePointInds.indices.size() > 1){
  pcl::PointCloud<PointT> table;
  table.height = 1; 
  table.width = tablePointInds.indices.size();
  table.points.resize(table.height * table.width);
  for(int i = 0; i < tablePointInds.indices.size(); i ++){
    table.points.at(i).x = cloud.points.at(tablePointInds.indices.at(i)).x;
    table.points.at(i).y = cloud.points.at(tablePointInds.indices.at(i)).y;
    table.points.at(i).z = cloud.points.at(tablePointInds.indices.at(i)).z;
    table.points.at(i).rgb = cloud.points.at(tablePointInds.indices.at(i)).rgb;
  }
    pcl::io::savePCDFile("table.pcd", table);
  }
}

void createPointCloud(int ***IMAGE, string transformfile, pcl::PointCloud<PointT> &cloud, map<int, int> &tablePoints) {
    int index = 0;
    ColorRGB color(0, 0, 0);

    cloud.height = 1;
    cloud.width = X_RES*Y_RES;
    cloud.points.resize(cloud.height * cloud.width);

    for (int y = 0; y < Y_RES; y++) {
        for (int x = 0; x < X_RES; x++) {
            color.assignColor(float(IMAGE[x][y][0]) / 255.0, float(IMAGE[x][y][1]) / 255, float(IMAGE[x][y][2]) / 255);
            cloud.points.at(index).y = IMAGE[x][y][3];
            cloud.points.at(index).x = (x - 640 * 0.5) * cloud.points.at(index).y * 1.1147 / 640;
            cloud.points.at(index).z = (480 * 0.5 - y) * cloud.points.at(index).y * 0.8336 / 480;
            cloud.points.at(index).rgb = color.getFloatRep();
            index++;
        }
    }
    
    
    TransformG globalTransform;
    globalTransform = readTranform(transformfile);
    globalTransform.transformPointCloudInPlaceAndSetOrigin(cloud);
    // find table indices
    pcl::PointIndices tablePointInds;
    getTableInds(cloud, tablePointInds);
    //saveTablePC(cloud, tablePointInds);

    cout << "size of table :" << tablePointInds.indices.size() << endl;
    for (size_t i = 0; i < tablePointInds.indices.size(); i++)
        tablePoints[tablePointInds.indices.at(i)] = 1;

}


void filterCloud(pcl::PointCloud<PointT> &cloud, map<int, int> &tablePoints, string transformfile, pcl::PointIndices & objIndices, pcl::PointXYZ &centroid ) {

    // remove points too far from the camera (eg walls)
    PointT origin;
    origin.x = 0;
    origin.y = 0;
    origin.z = 0;
    TransformG globalTransform;
    globalTransform = readTranform(transformfile);
    globalTransform.transformPointInPlace(origin);
    vector<int> indices;
    cout << "cloud size: " << cloud.points.size() << " indicies:" << objIndices.indices.size() << endl; 
    pcl::PointIndices localIndices, clusterIndices;
    for (int i = 0; i < cloud.points.size(); i++) {
        double dist_from_cam = sqrt(sqr(origin.x - cloud.points[i].x) +
                sqr(origin.y - cloud.points[i].y) +
                sqr(origin.z - cloud.points[i].z));
        
        if (dist_from_cam < 3500 && dist_from_cam > 0 )
        { 
          if( tablePoints.find(i) == tablePoints.end()) {
            indices.push_back(i);
          }
          //else {cout << "table point " << i << endl;}
        }
    }
    pcl::PointCloud<PointT> temp_cloud;
    temp_cloud = cloud;
    cloud.points.resize(indices.size());
    cloud.width = indices.size();
    for (int i = 0; i < indices.size(); i++) {
        if (i != indices[i])
            cloud.points[i] = temp_cloud.points[indices[i]];
        localIndices.indices.push_back(objIndices.indices.at(indices[i]));
        
    }

    
    // cluster and then retain the biggest cluster
    getMaxConsistentCluster(cloud, clusterIndices, centroid);
    /// 
    objIndices.indices.clear();
    for(size_t i = 0 ; i < clusterIndices.indices.size(); i ++){
        objIndices.indices.push_back(localIndices.indices.at(clusterIndices.indices.at(i)));
    }
    cout << "size after filtering:" << objIndices.indices.size() << endl;


}

void checkIndices(pcl::PointCloud<PointT> & cloud, pcl::PointCloud<PointT> & fullcloud, pcl::PointIndices indices){
    
    for(size_t i = 0 ; i < indices.indices.size(); i ++)
    {
        assert(fullcloud.points.at(indices.indices.at(i)).x == cloud.points.at(i).x);
        assert(fullcloud.points.at(indices.indices.at(i)).y == cloud.points.at(i).y);
        assert(fullcloud.points.at(indices.indices.at(i)).z == cloud.points.at(i).z);
        assert(fullcloud.points.at(indices.indices.at(i)).rgb == cloud.points.at(i).rgb);
    }
}

int getObjectPointCloud(pcl::PointCloud<PointT> &fullcloud, map<int, int> &tablePoints, string transformfile, vector<double> features, pcl::PointIndices &objIndices, string fn, pcl::PointXYZ &centroid ) {
    double minX = features.at(2);
    double minY = features.at(3);
    double maxX = features.at(4);
    double maxY = features.at(5);
    if(maxY>480 || maxX>640){return -1;}
    
    pcl::PointCloud<PointT> cloud;
    
    int index = 0;
    cloud.height = 1;
    cloud.width = (maxY - minY + 1)*(maxX - minX + 1);
    cloud.points.resize(cloud.height * cloud.width);
    cout << "width" << cloud.width << endl;
     map<int, int> localTablePoints;
 // cout << "full cloud size : " << fullcloud.points.size() << " indices : " << objIndices.indices.size() <<   endl; 
  
    int objIndex = 0;
    for (int y = minY; y <= maxY; y++) {
        for (int x = minX; x <= maxX; x++) {
            index = y * X_RES + x - 1; //x*Y_RES +y; //:q
            
           // cout << "obj index " << objIndex << " index " << index << endl;
            //cloud.points.at(objIndex) = fullcloud.points.at(index);
            //objIndices.indices.push_back(index);
            if (tablePoints.find(index) == tablePoints.end()) {
            cloud.points.at(objIndex) = fullcloud.points.at(index);
            objIndices.indices.push_back(index);
            objIndex++;
            //    localTablePoints[objIndex] = 1;
            }
            //cout << cloud.points.at(objIndex).x << "," << cloud.points.at(objIndex).y << "," << cloud.points.at(objIndex).z << endl;
           // objIndex++;
        }
    }
     cloud.width = objIndices.indices.size();
    cloud.points.resize(objIndices.indices.size());
    cout << "cloud size : " << cloud.points.size() << " indices : " << objIndices.indices.size() << "objindex : " << objIndex<< " tablepoints: " << localTablePoints.size() <<  endl; 
    if(cloud.points.size()>10){
        filterCloud(cloud,localTablePoints, transformfile, objIndices, centroid);
    
        cout << "size after filtering:" << objIndices.indices.size() << endl;
        checkIndices(cloud,fullcloud,objIndices);
    }
    string filename;
    //sprintf(filename, "%s_obj_%d.pcd",aid, objID);
    filename = "pointclouds/"+fn;
    pcl::io::savePCDFileBinary(filename, cloud);
    std::cerr << "Saved " << cloud.points.size() << " data points to " << filename << std::endl;
    return 1;
}

/*
 * 
 */
int main(int argc, char** argv) {

    dataLocation =  (string)argv[1] + "/";
    string mirrored_dataLocation = "";//"data/"; //+ (string)argv[1] + "_m/";
    actfile = (string)argv[2];//"activityLabel.txt";
    readDataActMap();


    // get all names of file from the map
    vector<string> all_files;
    map<string, string>::iterator it = data_act_map.begin();
    while (it != data_act_map.end()) {
        all_files.push_back(it->first);
        it++;
    }
    printf("Number of Files to be processed = %d\n", all_files.size());


  
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


    //fileList[1] = "data/0829113826_obj_2.txt";
    vector<vector<double> > objData;
    string lastActId = "0";
    for (size_t i = 0; i < all_files.size(); i++) {
        int count = 1;

        vector <string> fileList(data_obj_map[all_files.at(i)].size());
        for (size_t j = 0; j < data_obj_map[all_files.at(i)].size(); j++) {
            fileList.at(j) = dataLocation + "/" + all_files.at(i) + "_obj" + data_obj_map[all_files.at(i)].at(j) + ".txt";
        }
         
        
        const string transformfile = dataLocation + all_files[i] + "_globalTransform.txt";

        // for both mirrored and non mirrored data make j<2 ; for now use only mirrored
        for (int j = 0; j < 1; j++) {
            Frame::FrameNum = 0;
            bool mirrored = (j == 0) ? false : true;
            bool skipOdd = false;
            readData* DATA = new readData(dataLocation, all_files[i], data_act_map, i + 1, mirrored, mirrored_dataLocation, skipOdd, fileList);
            objData.clear();
            int status = DATA->readNextFrame(data, pos_data, data_CONF, pos_data_CONF, IMAGE, objData);


           while(status <130 ) {
               status = DATA->readNextFrame(data, pos_data, data_CONF, pos_data_CONF, IMAGE, objData);
           }
           pcl::PointXYZ centroid (0,0,0);
           while (status > 0) {
              
                // create point cloud
                pcl::PointCloud<PointT> cloud;

                map<int, int> tablePoints;
                createPointCloud(IMAGE, transformfile, cloud, tablePoints);
                // for each object find the object point cloud
                for (size_t o = 0; o < objData.size(); o++) {
                    pcl::PointIndices cloudInds;
                    stringstream fn; 
                    fn << all_files[i] + "_frame_";
                    fn << status;
                    fn << "_obj_";
                    fn << o; 
                    fn << ".pcd";
                    int rval = getObjectPointCloud(cloud,tablePoints,transformfile,objData.at(o),cloudInds, fn.str(), centroid);
                    // write the object point cloud indices.
                    std::ofstream ofile;
                    std::stringstream onum;
                    onum << o+1;
                    if(rval == -1){
                        cout << "ERROR IN BOUNDING BOX action: " << all_files[i] << " obj :" << onum.str() << " fnum: " << status << endl;
                    }
                    
                    string fname = dataLocation + "/objects/" + all_files.at(i) + "_obj" +  onum.str() + ".txt";
                    ofile.open(fname.c_str(), std::fstream::app);
                    ofile << all_files[i] << "," << status << "," << onum.str() << "," ;
                    for(size_t t = 0; t < cloudInds.indices.size(); t ++){
                        ofile << cloudInds.indices.at(t) << ",";
                    }
                    ofile << endl;
                    ofile.close();
                }
                status = DATA->readNextFrame(data, pos_data, data_CONF, pos_data_CONF, IMAGE, objData);

                count++;
            }
        }
       
    }

    printf("ALL DONE.\n\n");

    return 0;
}

