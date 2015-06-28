/*
Copyright (C) 2012 Hema Koppula
*/

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
map<string, vector<string> > data_obj_type_map;


void errorMsg(string message) {
  cout << "ERROR! " << message << endl;
  exit(1);
}

void parseChk(bool chk) {
  if (!chk) {
    errorMsg("parsing error.");
  }
}

void readDataActMap(string actfile) {
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




void readDataActMapOld() {
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

int main(int argc, char **argv) {
  srand(time(0));
  int method = atoi(argv[3]);
  float threshold = atof(argv[4]);
  dataLocation = argv[1];
  string actfile = (string) argv[2];
  readDataActMap(actfile);
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
    readData* DATA = new readData(dataLocation, all_files.at(i));
    Segmentation_skel segSkel;
    int status = 1;
    string transformfile = dataLocation+ all_files.at(i) + "_globalTransform.txt";
    do {
      status = DATA->readNextFrame(data, pos_data, data_CONF, pos_data_CONF);
      if (status != 0)
        segSkel.addSkelFrame(data, pos_data, transformfile);
        cout << "status = " << status << endl;
    } while (status > 0);

    segSkel.computeSegmentsDynamic(threshold,method);
    segmentfile << all_files.at(i) << ";";
    segSkel.printSegments(segmentfile);

  }
  segmentfile.close();
}
