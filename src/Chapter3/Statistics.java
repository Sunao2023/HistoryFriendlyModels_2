package Chapter3;

import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all elements to store and produce the relevant         *
 * statistics from the simulation model in the case of a single run or of     *
 * multiple runs                                                              */
class Statistics {
    
    // TECHNICAL VARIABLES AND OBJECTS
    C3Model   model;
    /* Access to simulation data                                              */
    DataOutputStream fileOutput;
    /* Output file object of a single or multiple simulation                  */
    
    // STATS VARIABLES
    /* These elements are used in both the single and the multiple runs       *
     * simulation. They can be used to reproduce exactly figures 3.6-3.9 and  *
     * with suitable changes in the values of parameters figures 3.10-3.13    */
    ArrayList<Double>   herf_LO;
    /* Storage of herfindahl index in LO                                      */
    ArrayList<Double>   herf_SUI;
    /* Storage of herfindahl index in SUI                                     */
    ArrayList<Double>   enterFirms_1st_LO;
    /* Storage of number of first-generation firms in LO                      */
    ArrayList<Double>   enterFirms_2nd_LO;
    /* Storage of number of second-generation firms in LO                     */
    ArrayList<Double>   enterFirms_2nd_SUI;
    /* Storage of number of second-generation firms in SUI                    */
    ArrayList<Double>   enterFirms_3rd_SUI;
    /* Storage of number of diversified firms in SUI                          */
    ArrayList<Double>   share_1st_LO;
    /* Storage of market share of first-generation firms in LO                */
    ArrayList<Double>   share_2nd_LO;
    /* Storage of market share of second-generation firms in LO               */
    ArrayList<Double>   share_3rd_SUI;
    /* Storage of market share of diversified firms in SUI                    */
    ArrayList<Double>   share_2nd_SUI;
    /* Storage of market share of second-generation firms in SUI              */
    ArrayList<Double>   share_best2nd_SUI;
    /* Storage of market share of the best second-generation firms in SUI     */
    
    /* These elements are used only in the single run simulation. They can be *
     * used to have a closer look in the dynamics of single simulation run.   *
     * Performance and cheapness data can be used to reconstruct firm         *
     * trajectories in the technological space, as in figures 3.3-3.5         */
    ArrayList[] singleShare;
    /* Storage of individual firms market share                               */
    ArrayList[] singleMod;
    /* Storage of individual firms mod                                        */
    ArrayList[] singleCheapness;
    /* Storage of individual firms cheapness                                  */
    ArrayList[] singlePerformance;
    /* Storage of individual firms performance                                */
    ArrayList[] singleServedUserClass;
    /* Storage of individual firms served user class (LO: Large Organizations *
     * SUI: Small Users and Individuals NONE: the firm never entered          */
    
    // CONSTRUCTOR
    Statistics(C3Model MODEL, boolean isSingle) {
    
        model      = MODEL;
        
        herf_LO            = new ArrayList<Double>();
        herf_SUI           = new ArrayList<Double>();
        enterFirms_1st_LO  = new ArrayList<Double>();
        enterFirms_2nd_LO  = new ArrayList<Double>();
        enterFirms_2nd_SUI = new ArrayList<Double>();
        enterFirms_3rd_SUI = new ArrayList<Double>();
        share_1st_LO       = new ArrayList<Double>();
        share_2nd_LO       = new ArrayList<Double>();
        share_3rd_SUI      = new ArrayList<Double>();
        share_2nd_SUI      = new ArrayList<Double>();
        share_best2nd_SUI  = new ArrayList<Double>(); 
        
        /* This initialization is required in case of single simulation       */
        if (isSingle) {
            
            singleShare           = new ArrayList[model.endTime];
            singleMod             = new ArrayList[model.endTime];
            singleCheapness       = new ArrayList[model.endTime];
            singlePerformance     = new ArrayList[model.endTime];
            singleServedUserClass = new ArrayList[model.endTime];
            
            for (int t = 0; t < model.endTime; t++) {
                singleShare[t]           = new ArrayList();
                singleMod[t]             = new ArrayList();
                singleCheapness[t]       = new ArrayList();
                singlePerformance[t]     = new ArrayList();
                singleServedUserClass[t] = new ArrayList();
            }
        }
        /* This initialization is required in case of multiple simulation     */
        else {
            for (int t = 0; t <= model.endTime; t++) {
                herf_LO.add(0.0);
                herf_SUI.add(0.0);
                enterFirms_1st_LO.add(0.0);
                enterFirms_2nd_LO.add(0.0);
                enterFirms_2nd_SUI.add(0.0);
                enterFirms_3rd_SUI.add(0.0);
                share_1st_LO.add(0.0);
                share_2nd_LO.add(0.0);
                share_3rd_SUI.add(0.0);
                share_2nd_SUI.add(0.0);
                share_best2nd_SUI.add(0.0);
            }
        }
    }
    
    /* This is a method to close the output file object                       */
    void closeFile() {
        try {
            fileOutput.flush();
            fileOutput.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    /* This is a method to initialize the output file object                  */
    void openFile(String nameOutput) {
        try {
            fileOutput = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameOutput)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    /* This is an ancillary method to write data in the output file object    */
    void print(String str) {
        try {
            fileOutput.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    /* This method gets data from the current simulation run and stores them  *
    * into the storage objects in case of a single simulation                 */
    void makeSingleStatistics() {
        
        for (int f = 1; f <= model.computerIndustry.numberOfFirms; f++) {
            singleShare[model.timer-1].add(model.computerIndustry.firms[f].share);
            singleMod[model.timer-1].add(model.computerIndustry.firms[f].mod);
            singleCheapness[model.timer-1].add(model.computerIndustry.firms[f].computer.cheap);
            singlePerformance[model.timer-1].add(model.computerIndustry.firms[f].computer.perf);
            if (!model.computerIndustry.firms[f].entered) {
                singleServedUserClass[model.timer-1].add("NONE");
            }
            else {
                if (model.computerIndustry.firms[f].servedUserClass == model.largeOrgs) {
                    singleServedUserClass[model.timer-1].add("LO");
                }
                if (model.computerIndustry.firms[f].servedUserClass == model.smallUsers) {
                    singleServedUserClass[model.timer-1].add("SUI");
                }
            }
        }

        herf_LO.add(model.largeOrgs.herfindahl);
        herf_SUI.add(model.smallUsers.herfindahl);
        enterFirms_1st_LO.add(model.largeOrgs.numOfFirstGenFirms);
        enterFirms_2nd_LO.add(model.largeOrgs.numOfSecondGenFirms);
        enterFirms_2nd_SUI.add(model.smallUsers.numOfSecondGenFirms);
        enterFirms_3rd_SUI.add(model.smallUsers.numOfDiversifiedFirms);
        share_1st_LO.add(model.largeOrgs.share1stGen);
        share_2nd_LO.add(model.largeOrgs.share2ndGen);
        share_2nd_SUI.add(model.smallUsers.share2ndGen);
        share_best2nd_SUI.add(model.smallUsers.shareBest2nd);
        share_3rd_SUI.add(model.smallUsers.shareDiv);
    }
    
    /* This method gets data from the current simulation run and stores them  *
     * into the storage objects in case of a multiple simulation              */
    void makeStatistics() {
          herf_LO.set(model.timer, herf_LO.get(model.timer) + (model.largeOrgs.herfindahl/model.multiTime));
          herf_SUI.set(model.timer, herf_SUI.get(model.timer) + (model.smallUsers.herfindahl/model.multiTime));
          enterFirms_1st_LO.set(model.timer, enterFirms_1st_LO.get(model.timer) + (model.largeOrgs.numOfFirstGenFirms/model.multiTime));
          enterFirms_2nd_LO.set(model.timer, enterFirms_2nd_LO.get(model.timer) + (model.largeOrgs.numOfSecondGenFirms/model.multiTime));
          enterFirms_2nd_SUI.set(model.timer, enterFirms_2nd_SUI.get(model.timer) + (model.smallUsers.numOfSecondGenFirms/model.multiTime));
          enterFirms_3rd_SUI.set(model.timer, enterFirms_3rd_SUI.get(model.timer) + (model.smallUsers.numOfDiversifiedFirms/model.multiTime));
          share_1st_LO.set(model.timer, share_1st_LO.get(model.timer) + (model.largeOrgs.share1stGen/model.multiTime));
          share_2nd_LO.set(model.timer, share_2nd_LO.get(model.timer) + (model.largeOrgs.share2ndGen/model.multiTime));
          share_2nd_SUI.set(model.timer,share_2nd_SUI.get(model.timer) + (model.smallUsers.share2ndGen/model.multiTime));
          share_best2nd_SUI.set(model.timer, share_best2nd_SUI.get(model.timer) + (model.smallUsers.shareBest2nd/model.multiTime));
          share_3rd_SUI.set(model.timer, share_3rd_SUI.get(model.timer) + (model.smallUsers.shareDiv/model.multiTime));
    }

    /* This method writes data in the output file in case of multiple         *
     * simulation                                                             */
    void printMultiStatistics() {
        
        print("Herfindahl in PC and mainframe markets\n");
        print("MF;");
        for (int t = 1; t <= model.endTime; t++) {
            print(herf_LO.get(t) + ";");
        }
        print("\n");
        print("PC;");
        for (int t = 1; t <= model.endTime; t++) {
            print(herf_SUI.get(t) + ";");
        }
        print("\n");

        print("\nNumber of firms in mainframe market\n");
        print("1st gen firms;");
        for (int t = 1; t <= model.endTime; t++) {
            print(enterFirms_1st_LO.get(t) + ";");
        }
        print("\n");
        print("2nd gen firms;");
        for (int t = 1; t <= model.endTime; t++) {
            print(enterFirms_2nd_LO.get(t) + ";");
        }
        print("\n");     
        print("Total number;");
        for (int t = 1; t <= model.endTime; t++) {
            double totalMF = enterFirms_1st_LO.get(t) + enterFirms_2nd_LO.get(t);
            print(totalMF + ";");
        }
        print("\n");               
        
        print("\nNumber of firms in PC market\n");
        print("MP start-ups;");
        for (int t = 1; t <= model.endTime; t++) {
            print(enterFirms_2nd_SUI.get(t) + ";");
        }
        print("\n");
        print("Diversified firms;");
        for (int t = 1; t <= model.endTime; t++) {
            print(enterFirms_3rd_SUI.get(t) + ";");
        }
        print("\n");
        print("Total number;");
        for (int t = 1; t <= model.endTime; t++) {
            double totalPC = enterFirms_2nd_SUI.get(t) + enterFirms_3rd_SUI.get(t);
            print(totalPC + ";");
        }
        print("\n");

        print("\nMarket share in PC market\n");
        print("Total MP start-ups;");
        for (int t = 1; t <= model.endTime; t++) {
            print(share_2nd_SUI.get(t) + ";");
        }
        print("\n");
        print("Diversified firms;");
        for (int t = 1; t <= model.endTime; t++) {
            print(share_3rd_SUI.get(t) + ";");
        }
        print("\n");
        print("Best MP start-up;");
        for (int t = 1; t <= model.endTime; t++) {
            print(share_best2nd_SUI.get(t) + ";");
        }
        print("\n");
        
        print("\nMarket share in Mainframe market\n");
        print("1st gen firms;");
        for (int t = 1; t <= model.endTime; t++) {
            print(share_1st_LO.get(t) + ";");
        }
        print("\n");
        print("2nd gen firms;");
        for (int t = 1; t <= model.endTime; t++) {
            print(share_2nd_LO.get(t) + ";");
        }
        print("\n");
    }

    /* This method writes data in the output file in case of single           *
     * simulation                                                             */
    void printSingleStatistics() {
        
        print("Main Statistics\n");
        print("\n");
        print("T;HLO;F1stLO;F2ndLO;S1stLO;S2ndLO;HSUI;F2ndSUI;F3rdSUI;S2ndSUI;S3rdSUI;SB2ndSUI\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t+";");
            print(herf_LO.get(t-1)+";");
            print(enterFirms_1st_LO.get(t-1)+";");
            print(enterFirms_2nd_LO.get(t-1)+";");
            print(share_1st_LO.get(t-1)+";");
            print(share_2nd_LO.get(t-1)+";");
            print(herf_SUI.get(t-1)+";");
            print(enterFirms_2nd_SUI.get(t-1)+";");
            print(enterFirms_3rd_SUI.get(t-1)+";");
            print(share_2nd_SUI.get(t-1)+";");
            print(share_3rd_SUI.get(t-1)+";");
            print(share_best2nd_SUI.get(t-1)+"\n");
        }
        
        print("\nComputerFirm MOD\n");
        print("FIRM;");
        for (int f = 1; f <= singleMod[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        print("T;");
        for (int f = 1; f <= singleMod[model.endTime-1].size(); f++) {
            print(singleServedUserClass[model.endTime-1].get(f-1).toString() + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleMod[t-1].size(); f++) {
                print(singleMod[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }

        print("\nComputerFirm SHARE \n");
        print("FIRM;");
        for (int f = 1; f <= singleShare[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        print("T;");
        for (int f = 1; f <= singleMod[model.endTime-1].size(); f++) {
            print(singleServedUserClass[model.endTime-1].get(f-1).toString() + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleShare[t-1].size(); f++) {
                print(singleShare[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
        
        print("\nComputerFirms Cheapness \n");
        print("FIRM;");
        for (int f = 1; f <= singleCheapness[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        print("T;");
        for (int f = 1; f <= singleMod[model.endTime-1].size(); f++) {
            print(singleServedUserClass[model.endTime-1].get(f-1).toString() + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleCheapness[t-1].size(); f++) {
                print(singleCheapness[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }

        print("\nComputerFirms Performance \n");
        print("FIRM;");
        for (int f = 1; f <= singlePerformance[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        print("T;");
        for (int f = 1; f <= singleMod[model.endTime-1].size(); f++) {
            print(singleServedUserClass[model.endTime-1].get(f-1).toString() + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singlePerformance[t-1].size(); f++) {
                print(singlePerformance[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
    }
}