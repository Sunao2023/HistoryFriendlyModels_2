package Chapter4;

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
    C4Model   model;
    /* Access to simulation data                                              */
    DataOutputStream fileOutput;
    /* Output file object of a single or multiple simulation                  */
    
    // STATS VARIABLES
    /* These elements are used in both the single and the multiple runs       *
     * simulation. They can be used to reproduce exactly figure 4.1 and with  *
     * suitable changes in the values of parameters figures 4.2-4.5           */
    ArrayList<Double>   aliveFirms_MF;
    /* Storage of number of active firms in Mainframes market                 */
    ArrayList<Double>   aliveFirms_PC;
    /* Storage of number of active firms in PC market                         */
    ArrayList<Double>   aliveFirms_CMP;
    /* Storage of number of active firms in Component market                  */
    ArrayList<Double>   herf_MF;
    /* Storage of herfindahl index in Mainframes market                       */
    ArrayList<Double>   herf_PC;
    /* Storage of herfindahl index in PC market                               */
    ArrayList<Double>   herf_CMP;
    /* Storage of herfindahl index in Component market                        */
    ArrayList<Double>   intFirms_MF;
    /* Storage of number of integrated firms in Mainframes market             */
    ArrayList<Double>   intFirms_PC;
    /* Storage of number of integrated firms in PC market                     */
    ArrayList<Double>   intRatio_MF;
    /* Storage of integration ratio in Mainframes market                      */
    ArrayList<Double>   intRatio_PC;
    /* Storage of integration ratio in PC market                              */
    
    /* These elements are used only in the single run simulation. They can be *
     * used to have a closer look in the dynamics of single simulation run.   */
    ArrayList[] singleShare_MF;
    /* Storage of individual firms market share in Mainframes market          */
    ArrayList[] singleShare_PC;
    /* Storage of individual firms market share in PC market                  */
    ArrayList[] singleShare_CMP;
    /* Storage of individual firms market share in Component market           */
    ArrayList[] singleMod_MF;
    /* Storage of individual firms mod in Mainframes market                   */
    ArrayList[] singleMod_PC;
    /* Storage of individual firms mod in PC market                           */
    ArrayList[] singleMod_CMP;
    /* Storage of individual firms mod in Component market                    */
    ArrayList[] singleSupplier_MF;
    /* Storage of supplier identifier in Mainfraems market                    */
    ArrayList[] singleSupplier_PC;
    /* Storage of supplier identifier in PC market                            */
    ArrayList[] singleNumOfBuyers_CMP;
    /* Storage of number of buying computer firms in Component market         */

    // CONSTRUCTOR
    Statistics(C4Model MODEL, boolean isSingle) {
    
        model      = MODEL;
                
        aliveFirms_MF  = new ArrayList<Double>();
        aliveFirms_PC  = new ArrayList<Double>();
        aliveFirms_CMP = new ArrayList<Double>();
        herf_MF        = new ArrayList<Double>();
        herf_PC        = new ArrayList<Double>();
        herf_CMP       = new ArrayList<Double>();
        intFirms_MF    = new ArrayList<Double>();
        intFirms_PC    = new ArrayList<Double>();
        intRatio_MF    = new ArrayList<Double>();
        intRatio_PC    = new ArrayList<Double>();
        
        /* This initialization is required in case of single simulation       */
        if (isSingle) {
            
            singleShare_MF        = new ArrayList[model.endTime];
            singleShare_PC        = new ArrayList[model.endTime];
            singleShare_CMP       = new ArrayList[model.endTime];
            singleMod_MF          = new ArrayList[model.endTime];
            singleMod_PC          = new ArrayList[model.endTime];
            singleMod_CMP         = new ArrayList[model.endTime];
            singleSupplier_MF     = new ArrayList[model.endTime];
            singleSupplier_PC     = new ArrayList[model.endTime];
            singleNumOfBuyers_CMP = new ArrayList[model.endTime];
            
            
            for (int t = 0; t < model.endTime; t++) {
                singleShare_MF[t]        = new ArrayList();
                singleMod_MF[t]          = new ArrayList();
                singleSupplier_MF[t]     = new ArrayList();
                singleShare_PC[t]        = new ArrayList();
                singleMod_PC[t]          = new ArrayList();
                singleSupplier_PC[t]     = new ArrayList();
                singleShare_CMP[t]       = new ArrayList();
                singleMod_CMP[t]         = new ArrayList();
                singleNumOfBuyers_CMP[t] = new ArrayList();
            }
        }
        /* This initialization is required in case of multiple simulation     */
        else {
            for (int t = 0; t <= model.endTime; t++) {
                aliveFirms_MF.add(0.0);
                aliveFirms_PC.add(0.0);
                aliveFirms_CMP.add(0.0);
                herf_MF.add(0.0);
                herf_PC.add(0.0);
                herf_CMP.add(0.0);
                intFirms_MF.add(0.0);
                intFirms_PC.add(0.0);
                intRatio_MF.add(0.0);
                intRatio_PC.add(0.0);
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
        
        for (int f = 1; f <= model.MFMarket.numOfFirms; f++) {
            singleMod_MF[model.timer-1].add(model.MFMarket.Firm[f].Computer.mod);
            singleShare_MF[model.timer-1].add(model.MFMarket.Firm[f].share);

            if (!model.MFMarket.Firm[f].integrated) {
                singleSupplier_MF[model.timer-1].add(model.MFMarket.Firm[f].supplierId);
            } else {
                singleSupplier_MF[model.timer-1].add(-1);
            }
        }

        for (int f = 1; f <= model.PCMarket.numOfFirms; f++) {
            singleMod_PC[model.timer-1].add(model.PCMarket.Firm[f].Computer.mod);
            singleShare_PC[model.timer-1].add(model.PCMarket.Firm[f].share);

            if (!model.PCMarket.Firm[f].integrated) {
                singleSupplier_PC[model.timer-1].add(model.PCMarket.Firm[f].supplierId);
            } else {
                singleSupplier_PC[model.timer-1].add(-1);
            }
        }

        for (int f = 1; f <= model.CmpMarket.numOfFirms; f++) {
            singleMod_CMP[model.timer-1].add(model.CmpMarket.Firm[f].Component.mod);
            singleNumOfBuyers_CMP[model.timer-1].add(model.CmpMarket.Firm[f].howManyBuyersMF
                                       + model.CmpMarket.Firm[f].howManyBuyersPC);
            singleShare_CMP[model.timer-1].add(model.CmpMarket.Firm[f].share);
        }
        
        aliveFirms_MF.add(model.MFMarket.aliveFirms);
        aliveFirms_PC.add(model.PCMarket.aliveFirms);
        aliveFirms_CMP.add(model.CmpMarket.aliveFirms);
        herf_MF.add(model.MFMarket.herfindahlIndex);
        herf_PC.add(model.PCMarket.herfindahlIndex);
        herf_CMP.add(model.CmpMarket.herfindahlIndex);
        intFirms_MF.add(model.MFMarket.intFirms);
        intFirms_PC.add(model.PCMarket.intFirms);
        intRatio_MF.add(model.MFMarket.intRatio);
        intRatio_PC.add(model.PCMarket.intRatio);
    }

    /* This method gets data from the current simulation run and stores them  *
     * into the storage objects in case of a multiple simulation              */
    void makeStatistics() {
        
        herf_MF.set(model.timer, herf_MF.get(model.timer)+(model.MFMarket.herfindahlIndex/model.multiTime));
        herf_PC.set(model.timer, herf_PC.get(model.timer)+(model.PCMarket.herfindahlIndex/model.multiTime));
        herf_CMP.set(model.timer, herf_CMP.get(model.timer)+(model.CmpMarket.herfindahlIndex/model.multiTime));
        aliveFirms_MF.set(model.timer, aliveFirms_MF.get(model.timer)+(model.MFMarket.aliveFirms/model.multiTime));
        aliveFirms_PC.set(model.timer, aliveFirms_PC.get(model.timer)+(model.PCMarket.aliveFirms/model.multiTime));
        aliveFirms_CMP.set(model.timer, aliveFirms_CMP.get(model.timer)+(model.CmpMarket.aliveFirms/model.multiTime));
        intFirms_MF.set(model.timer, intFirms_MF.get(model.timer)+(model.MFMarket.intFirms/model.multiTime));
        intFirms_PC.set(model.timer, intFirms_PC.get(model.timer)+(model.PCMarket.intFirms/model.multiTime));
        intRatio_MF.set(model.timer, intRatio_MF.get(model.timer)+(model.MFMarket.intRatio/model.multiTime));
        intRatio_PC.set(model.timer, intRatio_PC.get(model.timer)+(model.PCMarket.intRatio/model.multiTime ));
    }

    /* This method writes data in the output file in case of multiple         *
     * simulation                                                             */
    void printMultiStatistics() {
        
        print("Herfindahl index \n");
        print("MF;");
        for (int t = 1; t <= model.endTime; t++) {
            print(herf_MF.get(t) + ";");
        }
        print("\n");
        print("PC;");
        for (int t = 1; t <= model.endTime; t++) {
            print(herf_PC.get(t) + ";");
        }
        print("\n");
        print("CMP;");
        for (int t = 1; t <= model.endTime; t++) {
            print(herf_CMP.get(t) + ";");
        }
        print("\n");
        
        print("\nNumber of Firms \n");
        print("MF;");
        for (int t = 1; t <= model.endTime; t++) {
            print(aliveFirms_MF.get(t) + ";");
        }
        print("\n");
        print("PC;");
        for (int t = 1; t <= model.endTime; t++) {
            print(aliveFirms_PC.get(t) + ";");
        }
        print("\n");
        print("CMP;");
        for (int t = 1; t <= model.endTime; t++) {
            print(aliveFirms_CMP.get(t) + ";");
        }
        print("\n");
        
        print("\nNumber of Integrated Firms\n");
        print("MF;");
        for (int t = 1; t <= model.endTime; t++) {
            print(intFirms_MF.get(t) + ";");
        }
        print("\n");
        print("PC;");
        for (int t = 1; t <= model.endTime; t++) {
            print(intFirms_PC.get(t) + ";");
        }
        print("\n");

        print("\n Integration Ratio (number of integrated F/total number of firms)\n");
        print("MF;");
        for (int t = 1; t <= model.endTime; t++) {
            print(intRatio_MF.get(t) + ";");
        }
        print("\n");
        print("PC;");
        for (int t = 1; t <= model.endTime; t++) {
            print(intRatio_PC.get(t) + ";");
        }
        print("\n");
    }

    /* This method writes data in the output file in case of single           *
     * simulation                                                             */
    void printSingleStatistics() {
        print("Main Statistics\n");
        print("\n");
        print("T;HMF;NMF;INMF;IRMF;HPC;NPC;INPC;IRPC;HCMP;NCMP\n");
        for (int t = 1; t < model.endTime; t++) {
            print(t+";");
            print(herf_MF.get(t-1)+";");
            print(aliveFirms_MF.get(t-1)+";");
            print(intFirms_MF.get(t-1)+";");
            print(intRatio_MF.get(t-1)+";");
            print(herf_PC.get(t-1)+";");
            print(aliveFirms_PC.get(t-1)+";");
            print(intFirms_PC.get(t-1)+";");
            print(intRatio_PC.get(t-1)+";");
            print(herf_CMP.get(t-1)+";");
            print(aliveFirms_CMP.get(t-1)+"\n");
        }
        
        print("\nComputerFirm MOD\n");
        print("T;");
        for (int f = 1; f <= singleMod_MF[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleMod_MF[t-1].size(); f++) {
                print(singleMod_MF[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }

        print("\nMFComputerFirm SHARE \n");
        print("T;");
        for (int f = 1; f <= singleShare_MF[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleShare_MF[t-1].size(); f++) {
                print(singleShare_MF[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
        
        print("\nMFComputerFirms Component supplier \n");
        print("T;");
        for (int f = 1; f <= singleSupplier_MF[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleSupplier_MF[t-1].size(); f++) {
                print(singleSupplier_MF[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
        
        print("\nPC Computer mod\n");
        print("T;");
        for (int f = 1; f <= singleMod_PC[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleMod_PC[t-1].size(); f++) {
                print(singleMod_PC[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
        
        print("\nPCComputerFirm SHARE \n");
        print("T;");
        for (int f = 1; f <= singleShare_PC[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleShare_PC[t-1].size(); f++) {
                print(singleShare_PC[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
                
        print("\nPC ComputerFirms Component supplier \n");
        print("T;");
        for (int f = 1; f <= singleSupplier_PC[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleSupplier_PC[t-1].size(); f++) {
                print(singleSupplier_PC[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
        
        print("\nComponentFirm MOD\n");
        print("T;");
        for (int f = 1; f <= singleMod_CMP[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleMod_CMP[t-1].size(); f++) {
                print(singleMod_CMP[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
        
        print("\nComponentFirms SHARE\n");
        print("T;");
        for (int f = 1; f <= singleShare_CMP[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleShare_CMP[t-1].size(); f++) {
                print(singleShare_CMP[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
        
        print("\nCMP num of buyers\n");
        print("T;");
        for (int f = 1; f <= singleNumOfBuyers_CMP[model.endTime-1].size(); f++) {
            print(f + ";");
        }
        print("\n");
        for (int t = 1; t <= model.endTime; t++) {
            print(t + ";");
            for (int f = 1; f <= singleNumOfBuyers_CMP[t-1].size(); f++) {
                print(singleNumOfBuyers_CMP[t-1].get(f-1).toString() + ";");
            }
            print("\n");
        }
    }

}
