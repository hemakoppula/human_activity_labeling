//#include "frame.cpp"
#include "constants.h"
#include <iostream>
#include <fstream>

class Segment {
public:
    vector<Frame> frames;
    vector<vector<double> > obj_features;
    vector<vector<double> > obj_obj_features;
    vector<double> skel_features;
    vector<vector<double> > skel_obj_features;
    FeaturesSkel* features_skeleton;
    int segmentId;

    Segment(vector<Frame> &f, int id) {
        frames = f;
        segmentId = id;
        bool mirrored = false;
        features_skeleton = new FeaturesSkel(mirrored);
    }

    Segment() {
        bool mirrored = false;
        segmentId = 0;
        features_skeleton = new FeaturesSkel(mirrored);
    }

    void reset(vector<Frame> &f, int id) {
        frames = f;
        segmentId = id;
        obj_features.clear();
        obj_obj_features.clear();
        skel_features.clear();
        skel_obj_features.clear();
        //features_skeleton->reset();
    }
    void clear() {
        frames.clear();
        segmentId = 0;
        obj_features.clear();
        obj_obj_features.clear();
        skel_features.clear();
        skel_obj_features.clear();
        features_skeleton->reset(false);
    }

    vector<double> computeSkelObjFeatures(const FrameSkel & skel, const ObjectProfile & obj) {
        vector<double> features;


        double dist = 0;
        for (size_t i = 0; i < skel.transformed_joints.size(); i++) {
            dist = pow((skel.transformed_joints.at(i).x - obj.centroid.x), 2);
            dist += pow((skel.transformed_joints.at(i).y - obj.centroid.y), 2);
            dist += pow((skel.transformed_joints.at(i).z - obj.centroid.z), 2);
            features.push_back(dist);
        }
        return features;
    }

    vector<double> computeObjObjFeatures(ObjectProfile & obj1,  ObjectProfile & obj2) {

        vector <double> features;
        //
        features.push_back(obj1.centroid.x - obj2.centroid.x);
        features.push_back(obj1.centroid.y - obj2.centroid.y);
        features.push_back(obj1.centroid.z - obj2.centroid.z);
        features.push_back(obj1.getDistanceSqrBwCentroids(obj2));
        return features;
    }

    void computeFrameObjPairFeatures(Frame &frame, vector<vector<double> >& features) {
        // for every pair of objects compute the objObj features

        for (size_t i = 0; i < frame.objects.size(); i++) {
            for (size_t j = 0; j < frame.objects.size(); j++) {
                if (i != j) {
                    features.push_back(vector<double> (0));
                    features.at(features.size() - 1) = computeObjObjFeatures(frame.objects.at(i), frame.objects.at(j));
                    // oofeatfile << frameNew->sequenceId << "," << frameNew->frameNum << "," << frameNew->objects.at(i).objID << "," << frameNew->objects.at(j).objID  ;
                    // print_feats(obj_obj_features.at(obj_obj_features.size()-1),oofeatfile);
                }
            }

        }
        //cout << "Object- Object Features:" << endl;
        //      print_feats(obj_obj_features);
    }

    void computeFrameSkelObjPairFeatures(Frame &frame,vector<vector<double> >& features ) {
        // for every pair of objects compute the objObj features

        for (size_t i = 0; i < frame.objects.size(); i++) {
            features.push_back(vector<double> (0));
            features.at(features.size() - 1) = computeSkelObjFeatures(frame.skeleton, frame.objects.at(i));
            //sofeatfile << frameNew->sequenceId << "," << frameNew->frameNum << "," << frameNew->objects.at(i).objID;
            //print_feats(skel_obj_features.at(skel_obj_features.size()-1),sofeatfile);
        }
        //  cout << "Skelton - Object Features:" << endl;

        //  print_feats(skel_obj_features);
    }

    void computeFrameObjFeatures(Frame &frame) {
        // centroid features
        for (size_t i = 0; i < frame.objects.size(); i++) {
            //obj_features.push_back(vector<double>(0));
            obj_features.at(i) = frame.objects.at(i).features;
            //frame->objects.at(i).printFeatures();
            obj_features.at(i).push_back(frame.objects.at(i).getCentroid().x);
            obj_features.at(i).push_back(frame.objects.at(i).getCentroid().y);
            obj_features.at(i).push_back(frame.objects.at(i).getCentroid().z);
            // ofeatfile << frameNew->sequenceId << "," << frameNew->frameNum << "," << frameNew->objects.at(i).objID;
            //print_feats(obj_features.at(i),ofeatfile);
            //cout << "centroid x:" << objects.at(i).getCentroid().x << " y:" << objects.at(i).getCentroid().y << " z:" << objects.at(i).getCentroid().z << endl;
        }
        //   print_feats(obj_features);

    }

    void getFeatures(bool normalize) {
        computeSkelObjPairFeatures(normalize);
        computeObjFeatures( normalize );
        computeSkelFeatures(normalize);
        computeObjPairFeatures(normalize);
    }

   void getAdditiveFeatures(bool normalize) {
        computeSkelObjPairFeatures(normalize);
        computeObjFeatures( normalize );
        computeSkelFeatures(normalize);
        computeObjPairFeatures(normalize);
    }

    void computeObjFeatures(bool normalize) {
        int numFrames = frames.size();
        Frame ff = frames.at(0);
        Frame fl = frames.at(frames.size() - 1);
        for (size_t i = 0; i < ff.objects.size(); i++) {
            obj_features.push_back(vector<double>(0));
        }
        computeFrameObjFeatures(frames.at(floor(frames.size() / 2)));
        //computeFrameObjFeatures(fl);
        // distance and displacement
        for (size_t i = 0; i < ff.objects.size(); i++) {
            if(normalize){
                obj_features.at(i).push_back((ff.objects.at(i).getCentroid().x - fl.objects.at(i).getCentroid().x)/numFrames);
                obj_features.at(i).push_back((ff.objects.at(i).getCentroid().y - fl.objects.at(i).getCentroid().y)/numFrames);
                obj_features.at(i).push_back((ff.objects.at(i).getCentroid().z - fl.objects.at(i).getCentroid().z)/numFrames);
                obj_features.at(i).push_back((ff.objects.at(i).getDistanceSqrBwCentroids(fl.objects.at(i)))/numFrames);
            }else {
                obj_features.at(i).push_back(ff.objects.at(i).getCentroid().x - fl.objects.at(i).getCentroid().x);
                obj_features.at(i).push_back(ff.objects.at(i).getCentroid().y - fl.objects.at(i).getCentroid().y);
                obj_features.at(i).push_back(ff.objects.at(i).getCentroid().z - fl.objects.at(i).getCentroid().z);
                obj_features.at(i).push_back(ff.objects.at(i).getDistanceSqrBwCentroids(fl.objects.at(i)));
            }
            double totalDistance = 0;

            for (size_t j = 1; j < frames.size(); j++) {
                totalDistance += frames.at(j - 1).objects.at(i).getDistanceSqrBwCentroids(frames.at(j).objects.at(i));
            }
            if(normalize) {totalDistance = totalDistance/numFrames;}
            obj_features.at(i).push_back(totalDistance);

        }
    }

    double getDistanceSqrBwPoints(pcl::PointXYZ &p1, pcl::PointXYZ &p2) {
        double dist = 0;
        dist = pow((p1.x - p2.x), 2);
        dist += pow((p1.y - p2.y), 2);
        dist += pow((p1.z - p2.z), 2);
        //  dist = sqrt(dist);
        return dist;
    }


    double getDistanceSqrBwPoints(pcl::PointXYZRGB &p1, pcl::PointXYZRGB &p2) {
        double dist = 0;
        dist = pow((p1.x - p2.x), 2);
        dist += pow((p1.y - p2.y), 2);
        dist += pow((p1.z - p2.z), 2);
        //  dist = sqrt(dist);
        return dist;
    }

    void computeSkelFeatures(bool normalize) {
        int numFrames = frames.size();
        bool started = false;
        bool added = false;
        Frame frame = frames.at(floor(frames.size() / 2));
        int numFeats=0;


        /*
         * for calculating features at more than one frame
         * for (size_t i = 0; i <frames.size()/2; i ++){
            features_skeleton->addData(frames.at(i).skeleton->data, frames.at(i).skeleton->pos_data);
        }*/

        started = features_skeleton->extractSkeletonFeature(frame.skeleton.data, frame.skeleton.pos_data);
        if (started) {
            skel_features = features_skeleton->getFeatureValues();
        }
        /*
        else {
            for (size_t i = frames.size()/2; i < frames.size()-1; i ++){
                features_skeleton->addData(frames.at(i).skeleton->data, frames.at(i).skeleton->pos_data);
            }
            added=true;
            features_skeleton->extractSkeletonFeature(frames.at(frames.size()-1).skeleton->data, frames.at(frames.size()-1).skeleton->pos_data);
            skel_features = features_skeleton->getFeatureValues();
        }
         */
        // distance and displacement
        FrameSkel sf = frames.at(0).skeleton;
        FrameSkel sl = frames.at(frames.size() - 1).skeleton;
        double dist;
        for (size_t i = 0; i < sf.transformed_joints.size(); i++) {
            double x = sf.transformed_joints.at(i).x - sl.transformed_joints.at(i).x;
            double y = sf.transformed_joints.at(i).y - sl.transformed_joints.at(i).y;
            double z = sf.transformed_joints.at(i).z - sl.transformed_joints.at(i).z;
            double distance = getDistanceSqrBwPoints(sf.transformed_joints.at(i), sl.transformed_joints.at(i));
            double totalDistance = 0;

            for (size_t j = 1; j < frames.size(); j++) {
                totalDistance += getDistanceSqrBwPoints(frames.at(j - 1).skeleton.transformed_joints.at(i), frames.at(j).skeleton.transformed_joints.at(i));
            }
            if(normalize){x = x/ numFrames; y = y/ numFrames; z = z /numFrames; distance = distance/numFrames; totalDistance = totalDistance/numFrames;}
            skel_features.push_back(x);
            skel_features.push_back(y);
            skel_features.push_back(z);
            skel_features.push_back(distance);
            skel_features.push_back(totalDistance);
        }
        /*
        if(!added){
            for (size_t i = frames.size() / 2; i < frames.size(); i++) {
                features_skeleton->addData(frames.at(i).skeleton->data, frames.at(i).skeleton->pos_data);
            }
        }
        skel_features.insert(skel_features.begin(),frame.rgbdskel_feats.begin(),frame.rgbdskel_feats.end());
        */
    }

    void computeSkelAdditiveFeatures(bool normalize) {
        int numFrames = frames.size();
        bool started = false;
        bool added = false;
        Frame frame = frames.at(floor(frames.size() / 2));
        int numFeats=0;


        /*
         * for calculating features at more than one frame
         * for (size_t i = 0; i <frames.size()/2; i ++){
            features_skeleton->addData(frames.at(i).skeleton->data, frames.at(i).skeleton->pos_data);
        }*/

        started = features_skeleton->extractSkeletonFeature(frame.skeleton.data, frame.skeleton.pos_data);
        if (started) {
            skel_features = features_skeleton->getFeatureValues();
        }
        /*
        else {
            for (size_t i = frames.size()/2; i < frames.size()-1; i ++){
                features_skeleton->addData(frames.at(i).skeleton->data, frames.at(i).skeleton->pos_data);
            }
            added=true;
            features_skeleton->extractSkeletonFeature(frames.at(frames.size()-1).skeleton->data, frames.at(frames.size()-1).skeleton->pos_data);
            skel_features = features_skeleton->getFeatureValues();
        }
         */
        // distance and displacement
        FrameSkel sf = frames.at(0).skeleton;
        FrameSkel sl = frames.at(frames.size() - 1).skeleton;
        double dist;
        for (size_t i = 0; i < sf.transformed_joints.size(); i++) {
            double x = sf.transformed_joints.at(i).x - sl.transformed_joints.at(i).x;
            double y = sf.transformed_joints.at(i).y - sl.transformed_joints.at(i).y;
            double z = sf.transformed_joints.at(i).z - sl.transformed_joints.at(i).z;
            double distance = getDistanceSqrBwPoints(sf.transformed_joints.at(i), sl.transformed_joints.at(i));
            double totalDistance = 0;

            for (size_t j = 1; j < frames.size(); j++) {
                totalDistance += getDistanceSqrBwPoints(frames.at(j - 1).skeleton.transformed_joints.at(i), frames.at(j).skeleton.transformed_joints.at(i));
            }
            if(normalize){x = x/ numFrames; y = y/ numFrames; z = z /numFrames; distance = distance/numFrames; totalDistance = totalDistance/numFrames;}
            skel_features.push_back(x);
            skel_features.push_back(y);
            skel_features.push_back(z);
            skel_features.push_back(distance);
            skel_features.push_back(totalDistance);
        }
        /*
        if(!added){
            for (size_t i = frames.size() / 2; i < frames.size(); i++) {
                features_skeleton->addData(frames.at(i).skeleton->data, frames.at(i).skeleton->pos_data);
            }
        }
        skel_features.insert(skel_features.begin(),frame.rgbdskel_feats.begin(),frame.rgbdskel_feats.end());
        */
    }

    void computeObjPairFeatures(bool normalize) {
        // for every frame compute the obj-obj pair features
        int numFrames = frames.size();
        vector<vector<vector<double> > > features;
        for (size_t i = 0; i < frames.size(); i++) {
            vector<vector<double> > feats;
            computeFrameObjPairFeatures(frames.at(i), feats);
            features.push_back(feats);
        }
        int numObjs = frames.at(0).objects.size();
        int objPairCount = 0;
        for (size_t i = 0; i < numObjs; i++) {
            for (size_t j = 0; j < numObjs; j++) {
                if (i != j) {
                    obj_obj_features.push_back(vector<double> (0));

                    vector<double> min(features.at(0).at(objPairCount).size(), FLT_MAX), max(features.at(0).at(objPairCount).size(), FLT_MIN);

                    for (size_t k = 0; k < frames.size(); k++) {
                        // store the features of the first , middle and last frames
                        if (k == 0 || k == frames.size() - 1 || k == floor((frames.size() - 1) / 2)) {
                            //a.insert(a.end(), b.begin(), b.end());
                            obj_obj_features.at(objPairCount).insert(obj_obj_features.at(objPairCount).end(),features.at(k).at(objPairCount).begin(),features.at(k).at(objPairCount).end());

                            //obj_obj_features.at(objPairCount).push_back(features.at(k).at(objPairCount));
                        }
                        // compute the min and max of distances and displacements
                        for (size_t z = 0; z < min.size(); z++) {
                            if (features.at(k).at(objPairCount).at(z) < min.at(z))
                                min.at(z) = features.at(k).at(objPairCount).at(z);
                            if (features.at(k).at(objPairCount).at(z) > max.at(z))
                                max.at(z) = features.at(k).at(objPairCount).at(z);
                        }
                    }
                    if(normalize){
                        for (size_t z = 0; z < min.size(); z++) {
                            min.at(z) = min.at(z)/numFrames;
                        }
                        for (size_t z = 0; z < max.size(); z++) {
                            max.at(z) = max.at(z)/numFrames;
                        }
                    }
                    // oofeatfile << frameNew->sequenceId << "," << frameNew->frameNum << "," << frameNew->objects.at(i).objID << "," << frameNew->objects.at(j).objID  ;
                    // print_feats(obj_obj_features.at(obj_obj_features.size()-1),oofeatfile);
                    obj_obj_features.at(objPairCount).insert(obj_obj_features.at(objPairCount).end(),min.begin(),min.end());
                    obj_obj_features.at(objPairCount).insert(obj_obj_features.at(objPairCount).end(),max.begin(),max.end());
                    objPairCount++;

                }
            }

        }
        //cout << "Object- Object Features:" << endl;
        //      print_feats(obj_obj_features);
    }

    void computeSkelObjPairFeatures(bool normalize) {
        // for every pair of objects compute the objObj features
        int numFrames = frames.size();
        vector<vector<vector<double> > > features;
        for (size_t i = 0; i < frames.size(); i++) {
            vector<vector<double> > feats;
            computeFrameSkelObjPairFeatures(frames.at(i), feats);
            features.push_back(feats);
        }
        int numObjs = frames.at(0).objects.size();
        int objCount = 0;
        for (size_t i = 0; i < numObjs; i++) {
            skel_obj_features.push_back(vector<double> (0));
            vector<double> min(features.at(0).at(objCount).size(), FLT_MAX), max(features.at(0).at(objCount).size(), FLT_MIN);


            for (size_t k = 0; k < frames.size(); k++) {
                // store the features of the first , middle and last frames
                if (k == 0 || k == frames.size() - 1 || k == floor((frames.size() - 1) / 2)) {
                    skel_obj_features.at(objCount).insert(skel_obj_features.at(objCount).end(), features.at(k).at(objCount).begin(), features.at(k).at(objCount).end());
                }
                // compute the min and max of distances and displacements
                for (size_t z = 0; z < min.size(); z++) {
                    if (features.at(k).at(objCount).at(z) < min.at(z))
                        min.at(z) = features.at(k).at(objCount).at(z);
                    if (features.at(k).at(objCount).at(z) > max.at(z))
                        max.at(z) = features.at(k).at(objCount).at(z);
                }
            }
            if (normalize) {
                for (size_t z = 0; z < min.size(); z++) {
                    min.at(z) = min.at(z) / numFrames;
                }
                for (size_t z = 0; z < max.size(); z++) {
                    max.at(z) = max.at(z) / numFrames;
                }
            }

            skel_obj_features.at(objCount).insert(skel_obj_features.at(objCount).end(), min.begin(), min.end());
            skel_obj_features.at(objCount).insert(skel_obj_features.at(objCount).end(), max.begin(), max.end());
            objCount++;
            //sofeatfile << frameNew->sequenceId << "," << frameNew->frameNum << "," << frameNew->objects.at(i).objID;
            //print_feats(skel_obj_features.at(skel_obj_features.size()-1),sofeatfile);
        }
        //  cout << "Skelton - Object Features:" << endl;

        //  print_feats(skel_obj_features);
    }


};

class FeaturesMultiFrame {
private:
    Segment segmentNew;
    Segment segmentOld;


    vector<double> skel_temporal_features;
    vector<vector<double> > obj_temporal_features;


    int segmentCount;


    //FeaturesSkelRGBD* features_rgbd;
    bool mirrored;
    bool temporal;
    bool temporalFlag;


    std::ofstream ofeatfile, sfeatfile, oofeatfile, sofeatfile, temporalSkelfeatfile, temporalObjfeatfile;

    void print_feats(vector<vector<double> > &feats) {
        for (size_t i = 0; i < feats.size(); i++) {
            cout << "object " << i << ":";
            for (size_t j = 0; j < feats.at(i).size(); j++) {
                cout << " " << feats.at(i).at(j);
            }
            cout << endl;
        }
    }

    void print_feats(vector<double> &feats, std::ofstream &file) {
        //cout << "feats: ";
        //file << "feats: ";
        for (size_t i = 0; i < feats.size(); i++) {
            //cout << " " << feats.at(i);
            file << "," << feats.at(i);
        }
        //cout << endl;
        file << endl;

    }

    void computeObjTemporalFeatures(bool normalize ) {

        Frame frameNew = segmentNew.frames.at(floor((segmentNew.frames.size()-1)/2));
        Frame frameOld = segmentOld.frames.at(floor((segmentOld.frames.size()-1)/2));
        int numFrame = frameNew.frameNum - frameOld.frameNum;
        for (size_t i = 0; i < frameNew.objects.size(); i++) {
            obj_temporal_features.push_back(vector<double>(0));

            //frame->objects.at(i).printFeatures();
            obj_temporal_features.at(i).push_back(frameNew.objects.at(i).getDistanceSqrBwCentroids(frameOld.objects.at(i)));
            obj_temporal_features.at(i).push_back(frameNew.objects.at(i).getVertDispCentroids(frameOld.objects.at(i)));
            if(normalize){
                obj_temporal_features.at(i).push_back((frameNew.objects.at(i).getDistanceSqrBwCentroids(frameOld.objects.at(i)))/numFrame);
                obj_temporal_features.at(i).push_back((frameNew.objects.at(i).getVertDispCentroids(frameOld.objects.at(i)))/numFrame);
            }
            //TODO : add transformation as a feature

            temporalObjfeatfile << frameNew.sequenceId << "," << segmentOld.segmentId << "," << segmentNew.segmentId << "," << frameNew.objects.at(i).objID;
            print_feats(obj_temporal_features.at(i), temporalObjfeatfile);
            //cout << "centroid x:" << objects.at(i).getCentroid().x << " y:" << objects.at(i).getCentroid().y << " z:" << objects.at(i).getCentroid().z << endl;
        }
        //print_feats(obj_temporal_features);
    }


    void computeObjTemporalFeaturesAdj(bool normalize ) {
        Frame frameNew = segmentNew.frames.at(0);
        Frame frameOld = segmentOld.frames.at(segmentOld.frames.size()-1);
        int numFrame = frameNew.frameNum - frameOld.frameNum;
        for (size_t i = 0; i < frameNew.objects.size(); i++) {
            obj_temporal_features.push_back(vector<double>(0));

            //frame->objects.at(i).printFeatures();
            obj_temporal_features.at(i).push_back(frameNew.objects.at(i).getDistanceSqrBwCentroids(frameOld.objects.at(i)));
            obj_temporal_features.at(i).push_back(frameNew.objects.at(i).getVertDispCentroids(frameOld.objects.at(i)));
            if(normalize){
                obj_temporal_features.at(i).push_back((frameNew.objects.at(i).getDistanceSqrBwCentroids(frameOld.objects.at(i)))/numFrame);
                obj_temporal_features.at(i).push_back((frameNew.objects.at(i).getVertDispCentroids(frameOld.objects.at(i)))/numFrame);
            }
            //TODO : add transformation as a feature

            temporalObjfeatfile << frameNew.sequenceId << "," << segmentOld.segmentId << "," << segmentNew.segmentId << "," << frameNew.objects.at(i).objID;
            print_feats(obj_temporal_features.at(i), temporalObjfeatfile);
            //cout << "centroid x:" << objects.at(i).getCentroid().x << " y:" << objects.at(i).getCentroid().y << " z:" << objects.at(i).getCentroid().z << endl;
        }
        //print_feats(obj_temporal_features);
    }


    void computeSkelTemporalFeatures(bool normalize) {
        Frame frameNew = segmentNew.frames.at(floor((segmentNew.frames.size()-1)/2));
        Frame frameOld = segmentOld.frames.at(floor((segmentOld.frames.size()-1)/2));
        int numFrame = frameNew.frameNum - frameOld.frameNum;
        // distance between of local joints positions
        for (size_t i = 0; i < frameNew.skeleton.num_local_joints; i++) {
            double dist = pow((frameNew.skeleton.joints_local[i][pos_data_x] - frameOld.skeleton.joints_local[i][pos_data_x]), 2) + pow((frameNew.skeleton.joints_local[i][pos_data_y] - frameOld.skeleton.joints_local[i][pos_data_y]), 2) + pow((frameNew.skeleton.joints_local[i][pos_data_z] - frameOld.skeleton.joints_local[i][pos_data_z]), 2);
            skel_temporal_features.push_back(dist);
            if(normalize){skel_temporal_features.push_back(dist/numFrame);}
        }
        temporalSkelfeatfile << frameNew.sequenceId << "," << segmentOld.segmentId << "," << segmentNew.segmentId;
        print_feats(skel_temporal_features, temporalSkelfeatfile);
    }

   void computeSkelTemporalFeaturesAdj(bool normalize) {
        Frame frameNew = segmentNew.frames.at(0);
        Frame frameOld = segmentOld.frames.at(segmentOld.frames.size()-1);
        int numFrame = frameNew.frameNum - frameOld.frameNum;
        // distance between of local joints positions
        for (size_t i = 0; i < frameNew.skeleton.num_local_joints; i++) {
            double dist = pow((frameNew.skeleton.joints_local[i][pos_data_x] - frameOld.skeleton.joints_local[i][pos_data_x]), 2) + pow((frameNew.skeleton.joints_local[i][pos_data_y] - frameOld.skeleton.joints_local[i][pos_data_y]), 2) + pow((frameNew.skeleton.joints_local[i][pos_data_z] - frameOld.skeleton.joints_local[i][pos_data_z]), 2);
            skel_temporal_features.push_back(dist);
            if(normalize){skel_temporal_features.push_back(dist/numFrame);}
        }
        temporalSkelfeatfile << frameNew.sequenceId << "," << segmentOld.segmentId << "," << segmentNew.segmentId;
        print_feats(skel_temporal_features, temporalSkelfeatfile);
   }

public:

    void writeObjObjFeats(){
        int numObjs = segmentNew.frames.at(0).objects.size();
        int objPairCount = 0;
        for(size_t i = 0; i < numObjs; i++){
            for (size_t j = 0; j < numObjs; j++){
                if(i!=j){
                    oofeatfile << segmentNew.frames.at(0).sequenceId << "," << segmentNew.segmentId << "," << segmentNew.frames.at(0).objects.at(i).objID << "," << segmentNew.frames.at(0).objects.at(j).objID  ;
                    print_feats(segmentNew.obj_obj_features.at(objPairCount),oofeatfile);
                    objPairCount++;
                }
            }

        }
    }
    void writeSkelObjFeats() {
        int numObjs = segmentNew.frames.at(0).objects.size();

        for(size_t i = 0; i < numObjs; i++){
        sofeatfile <<  segmentNew.frames.at(0).sequenceId << "," << segmentNew.segmentId << "," << segmentNew.frames.at(0).objects.at(i).objID;
            print_feats(segmentNew.skel_obj_features.at(i),sofeatfile);
        }
    }
    void writeSkelFeats(){

        sfeatfile << segmentNew.frames.at(0).sequenceId << "," << segmentNew.segmentId ;
        print_feats(segmentNew.skel_features,sfeatfile);
    }

    void writeObjFeats(){
        int numObjs = segmentNew.frames.at(0).objects.size();

        for(size_t i = 0; i < numObjs; i++){
            ofeatfile << segmentNew.frames.at(0).sequenceId  << "," << segmentNew.segmentId << "," << segmentNew.frames.at(0).objects.at(i).objID;
            print_feats(segmentNew.obj_features.at(i),ofeatfile);
        }
    }

    void computeFreatures(bool normalize) {

        segmentNew.getFeatures(normalize);

        if (temporal && temporalFlag) {
            computeTemporalFreatures(normalize);
            temporalFlag = false;
        }
        // write features
        writeObjFeats();
        writeSkelFeats();
        writeObjObjFeats();
        writeSkelObjFeats();
    }

    void computeTemporalFreatures(bool normalize) {

        obj_temporal_features.clear();
        skel_temporal_features.clear();
        computeObjTemporalFeatures(normalize);
        computeSkelTemporalFeatures(normalize);

    }

    void computeTemporalFreaturesAdj(bool normalize) {

        obj_temporal_features.clear();
        skel_temporal_features.clear();
        computeObjTemporalFeaturesAdj(normalize);
        computeSkelTemporalFeaturesAdj(normalize);

    }

    void resetActivity() {
        segmentNew.clear();
        segmentOld.clear();
        segmentCount = 0;
        temporalFlag = false;

    }

    void setCurrentSegment(vector<Frame> &s, int id) {
        segmentCount++;
        segmentOld.reset(segmentNew.frames, segmentNew.segmentId);
        segmentNew.reset(s, id);
        if(segmentCount > 1) {
            temporalFlag = true;
        }

    }

    FeaturesMultiFrame(bool Temporal) {
        mirrored = false;
        temporal = Temporal;
        segmentCount = 0;
        temporalFlag = false;
        ofeatfile.open("data_obj_feats.txt", ios::app);
        sfeatfile.open("data_skel_feats.txt", ios::app);
        oofeatfile.open("data_obj_obj_feats.txt", ios::app);
        sofeatfile.open("data_skel_obj_feats.txt", ios::app);
        if (temporal) {
            temporalObjfeatfile.open("data_temporal_obj_feats.txt", ios::app);
            temporalSkelfeatfile.open("data_temporal_skel_feats.txt", ios::app);
        }
        //  if (useSkeleton)


        //features_rgbd = new FeaturesSkelRGBD(mirrored);

    }

    ~FeaturesMultiFrame() {
        ofeatfile.close();
        sfeatfile.close();
        oofeatfile.close();
        sofeatfile.close();
        if (temporal) {
            temporalSkelfeatfile.close();
            temporalObjfeatfile.close();
        }

    }

};
