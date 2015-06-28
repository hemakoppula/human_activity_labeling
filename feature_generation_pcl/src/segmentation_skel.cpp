/*
Copyright (C) 2012 Hema Koppula
*/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <assert.h>

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

#include "./frame_skel.h"
#include "./segment-graph.h"

using namespace std;


class Segmentation_skel {
 private:
  vector<FrameSkel> skeletons;
  vector<vector<int> > segmentation;

  vector<double> get_displacement(const FrameSkel & skel1,
                                  const FrameSkel & skel2) {
    vector<double> displacement;
    for (size_t i = 0; i < skel1.num_local_joints; i++) {
      double distx = skel1.joints_local[i][pos_data_x]
                      - skel2.joints_local[i][pos_data_x];
      double disty = skel1.joints_local[i][pos_data_y]
                      - skel2.joints_local[i][pos_data_y];
      double distz = skel1.joints_local[i][pos_data_z]
                      - skel2.joints_local[i][pos_data_z];
      displacement.push_back(distx);
      displacement.push_back(disty);
      displacement.push_back(distz);
    }
    return displacement;
  }

  vector<double> get_vel(vector<double> disp1, vector<double> disp2) {
    vector<double> to_ret;
    for (size_t i = 0; i < disp1.size(); i++) {
      to_ret.push_back(disp2[i] - disp1[i]);
    }
    return to_ret;
  }

  float two_norm_squared(vector<double> disp1, vector<double> disp2) {
    double to_ret = 0.0;
    for (size_t i = 0; i < disp1.size(); i++) {
      to_ret += (disp1.at(i) - disp2.at(i))* (disp1.at(i) - disp2.at(i));
    }
    return to_ret;
  }

  float two_norm(vector<double> disp1) {
    double to_ret = 0.0;
    for (size_t i = 0; i < disp1.size(); i++) {
      to_ret += (disp1.at(i) )* (disp1.at(i) );
    }
    return to_ret;
  }

  void applyMedianFilter(int windowSize) {
    int numJoints = skeletons.at(0).num_local_joints;
    for (size_t i = windowSize/2; i < skeletons.size()-windowSize/2; i++) {
      for (int j = 0; j < numJoints; j++) {
        cout << j <<":" << endl;
        vector<double> x, y, z;
        for (int w = -windowSize/2; w <= windowSize/2; w ++) {
          cout << i+w << "," << endl;
          x.push_back(skeletons.at(i+w).joints_local[j][pos_data_x]);
          y.push_back(skeletons.at(i+w).joints_local[j][pos_data_y]);
          z.push_back(skeletons.at(i+w).joints_local[j][pos_data_z]);
        }
        std::sort(x.begin(), x.end());
        std::sort(y.begin(), y.end());
        std::sort(z.begin(), z.end());
        skeletons.at(i).joints_local[j][pos_data_x] = x[windowSize/2-1];
        skeletons.at(i).joints_local[j][pos_data_y] = y[windowSize/2-1];
        skeletons.at(i).joints_local[j][pos_data_z] = z[windowSize/2-1];
      }
    }
  }

 public:
  void addSkelFrame(double **data, double **pos_data, string transformFile) {
    FrameSkel sf(data, pos_data, transformFile);
    skeletons.push_back(sf);
  }

  void computeSegments() {
    cout << "number of frames so far: " << skeletons.size() << endl;
    int segnum = 0;
    segmentation.push_back(vector<int>());
    segmentation[segnum].push_back(0);
    for (size_t i = 1; i < skeletons.size(); i++) {
      cout << "skel " << i - 1 << " and " << i << endl;
      vector<double> dist = get_displacement(skeletons.at(i - 1),
                                             skeletons.at(i));
      bool flag = true;
      for (size_t j = 0; j < dist.size(); j++) {
        cout << "joint " << j << " , dist: " << dist.at(j) << endl;
        if (dist.at(j) > 2000) {
          flag = false;
        }
      }
      if (flag) {
        segmentation[segnum].push_back(i);
      } else {
        segnum++;
        segmentation.push_back(vector<int>());
        segmentation[segnum].push_back(i);
      }
    }
    // print the segments
    for (size_t i = 0; i < segmentation.size(); i++) {
        cout << "Segment " << i << " : ";
        for (size_t j = 0; j < segmentation.at(i).size(); j++) {
            cout << ", " << segmentation.at(i).at(j);
        }
        cout << endl;
    }
  }

  double getWeight(int A, int B, int C, int method) {
    double weight = 0;
    if (method == 1) {
      vector<double> distp = get_displacement(skeletons.at(A), skeletons.at(B));
      weight = two_norm(distp);
    } else if (method == 2) {
      vector<double> distp = get_displacement(skeletons.at(A), skeletons.at(B));
      vector<double> dista = get_displacement(skeletons.at(B), skeletons.at(C));
      weight = two_norm_squared(distp, dista);
    }

    return weight;
  }

  // Using algorithm and implementation
  // from http://www.cs.brown.edu/~pff/segment/
  // c is the thresholding parameter as described in the algorithm
  void computeSegmentsDynamic(float c, int method) {
    applyMedianFilter(3);
    cout << "number of frames so far: " << skeletons.size() << endl;
    universe * segmented_frames;

    // Create Graph, each frame maps to a node,
    // and each edge maps to the vector<double> disp1
    // distance between two skeletons
    edge * edges = new edge[skeletons.size() - 2];
    for (size_t i = 1; i < skeletons.size() - 1; i++) {
      cout << "skel " << i - 1 << " and " << i << endl;
      edges[(i - 1)].a = (i - 1);
      edges[(i - 1)].b = i;

      edges[(i - 1)].w = getWeight(i-1, i, i+1, method);
    }

    // Do segmentation based on the algorithm
    segmented_frames = segment_graph(skeletons.size() - 1,
                                     skeletons.size() - 2, edges, c);

    size_t cur_segment;
    // find all the skeleton's segments and setup the correct output
    for (size_t i = 0; i < skeletons.size() - 1; i++) {
      // To what segment does vertex i belong?
      cur_segment = (*segmented_frames).find(i);
      while (cur_segment >= segmentation.size()) {
        segmentation.push_back(vector<int>());
      }
      segmentation.at(cur_segment).push_back(i);
    }
  }
  void printSegments(std::ofstream &file) {
    // print the segments
    int segCount = 1;
    for (size_t i = 0; i < segmentation.size(); i++) {
      if (segmentation.at(i).size() > 0) {
        file << segCount << ":";
        file << segmentation.at(i).at(0)+1;
        for (size_t j = 1; j < segmentation.at(i).size(); j++) {
          if (j%50 == 0) {
            file << ";";
            segCount++;
            file << segCount << ":";
            file << segmentation.at(i).at(j)+1;
          } else {
            file << "," << segmentation.at(i).at(j)+1;
          }
        }
        file << ";";
        segCount++;
      }
    }
    file << endl;
  }

  Segmentation_skel() {}

  ~Segmentation_skel() {
    skeletons.clear();
    segmentation.clear();
  }
};
