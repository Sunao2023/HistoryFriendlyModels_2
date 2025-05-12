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
 * statistics from the simulation model in the case of sensitivity analysis   */
class SA_Statistics {

    // TECHNICAL VARIABLES AND OBJECTS
    C3Model model;
    /* Access to simulation data                                              */
    DataOutputStream fileSensHerf_LO;
    /* Output file object of herfindahl in LO                                 */
    String           nameSensHerf_LO;
    /* Name of the output file of herfindahl in LO                            */
    DataOutputStream fileSensHerf_SUI;
    /* Output file object of herfindahl in SUI                                */
    String           nameSensHerf_SUI;
    /* Name of the output file of herfindahl in SUI                           */
    DataOutputStream fileSensEnterFirms_1st_LO;
    /* Output file object of number of first-generation firms in LO           */
    String           nameSensEnterFirms_1st_LO;
    /* Name of the output file of number of first-generation firms in LO      */
    DataOutputStream fileSensEnterFirms_2nd_LO;
    /* Output file object of number of second-generation firms in LO          */
    String           nameSensEnterFirms_2nd_LO;
    /* Name of the output file of number of second-generation firms in LO     */
    DataOutputStream fileSensEnterFirms_3rd_SUI;
    /* Output file object of number of diversified firms in SUI               */
    String           nameSensEnterFirms_3rd_SUI;
    /* Name of the output file of number of diversified firms in SUI          */
    DataOutputStream fileSensEnterFirms_2nd_SUI;
    /* Output file object of number of second-generation firms in SUI         */
    String           nameSensEnterFirms_2nd_SUI;
    /* Name of the output file of number of second-generation firms in SUI    */
    DataOutputStream fileSensShare_2nd_SUI;
    /* Output file object of share of second-generation firms in SUI          */
    String           nameSensShare_2nd_SUI;
    /* Name of the output file of share of second-generation firms in SUI     */
    DataOutputStream fileSensShare_3rd_SUI;
    /* Output file object of share of diversified firms in SUI                */
    String           nameSensShare_3rd_SUI;
    /* Name of the output file of share of diversified firms in SUI           */
    DataOutputStream fileSensShare_best2nd_SUI;
    /* Output file object of share of best second-generation firms in SUI     */
    String           nameSensShare_best2nd_SUI;
    /* Name of the output file of share of best second-generation firms in SUI*/
    DataOutputStream fileSensShare_1st_LO;
    /* Output file object of share of first-generation firms in LO            */
    String           nameSensShare_1st_LO;
    /* Name of the output file of share of first-generation firms in LO       */
    DataOutputStream fileSensShare_2nd_LO;
    /* Output file object of share of second-generation firms in LO           */
    String           nameSensShare_2nd_LO;
    /* Name of the output file of share of second-generation firms in LO      */
    DataOutputStream fileSensParameters;
    /* Output file object of parameters                                       */
    String           nameSensParameters;
    /* Name of the output file of parameters                                  */
    
    // STATS VARIABLES
    ArrayList<String[]> sensHerf_LO;
    /* Storage of herfindahl index in LO                                      */
    ArrayList<String[]> sensHerf_SUI;
    /* Storage of herfindahl index in SUI                                     */
    ArrayList<String[]> sensEnterFirms_1st_LO;
    /* Storage of number of first-generation firms in LO                      */
    ArrayList<String[]> sensEnterFirms_2nd_LO;
    /* Storage of number of second-generation firms in LO                     */
    ArrayList<String[]> sensEnterFirms_3rd_SUI;
    /* Storage of number of diversified firms in SUI                          */
    ArrayList<String[]> sensEnterFirms_2nd_SUI;
    /* Storage of number of second-generation firms in SUI                    */
    ArrayList<String[]> sensShare_2nd_SUI;
    /* Storage of market share of second-generation firms in SUI              */
    ArrayList<String[]> sensShare_3rd_SUI;
    /* Storage of market share of diversified firms in SUI                    */
    ArrayList<String[]> sensShare_best2nd_SUI;
    /* Storage of market share of best second-generation firms in SUI         */
    ArrayList<String[]> sensShare_1st_LO;
    /* Storage of market share of first-generation firms in LO                */
    ArrayList<String[]> sensShare_2nd_LO;
    /* Storage of market share of second-generation firms in LO               */
    ArrayList<String[]> sensParameters;
    /* Storage of parameters used in the simulation runs                      */
    
    // CONSTRUCTOR
    SA_Statistics(C3Model MODEL) {
        
        model                      = MODEL;
        
        nameSensHerf_LO            = "/sa_herfLO.csv";
        nameSensHerf_SUI           = "/sa_herfSUI.csv";
        nameSensEnterFirms_1st_LO  = "/sa_firm1stLO.csv";
        nameSensEnterFirms_2nd_LO  = "/sa_firm2ndLO.csv";
        nameSensEnterFirms_3rd_SUI = "/sa_firm3rdSUI.csv";
        nameSensEnterFirms_2nd_SUI = "/sa_firm2ndSUI.csv";
        nameSensShare_2nd_SUI      = "/sa_share2ndSUI.csv";
        nameSensShare_3rd_SUI      = "/sa_share3rdSUI.csv";
        nameSensShare_best2nd_SUI  = "/sa_shareb2ndSUI.csv";
        nameSensShare_1st_LO       = "/sa_share1stLO.csv";
        nameSensShare_2nd_LO       = "/sa_share2ndLO.csv";
        nameSensParameters         = "/sa_parameters.csv";
        
        sensHerf_LO            = new ArrayList<String[]>();
        sensHerf_SUI           = new ArrayList<String[]>();
        sensEnterFirms_1st_LO  = new ArrayList<String[]>();
        sensEnterFirms_2nd_LO  = new ArrayList<String[]>();
        sensEnterFirms_3rd_SUI = new ArrayList<String[]>();
        sensEnterFirms_2nd_SUI = new ArrayList<String[]>();
        sensShare_2nd_SUI      = new ArrayList<String[]>();
        sensShare_3rd_SUI      = new ArrayList<String[]>();
        sensShare_best2nd_SUI  = new ArrayList<String[]>();
        sensShare_1st_LO       = new ArrayList<String[]>();
        sensShare_2nd_LO       = new ArrayList<String[]>();
        sensParameters         = new ArrayList<String[]>();
    }    
    
    /* This is a method to close the output file objects                      */
    void closeFile() {
        try {
            fileSensHerf_LO.flush();
            fileSensHerf_LO.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensHerf_SUI.flush();
            fileSensHerf_SUI.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensEnterFirms_1st_LO.flush();
            fileSensEnterFirms_1st_LO.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensEnterFirms_2nd_LO.flush();
            fileSensEnterFirms_2nd_LO.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensEnterFirms_3rd_SUI.flush();
            fileSensEnterFirms_3rd_SUI.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensEnterFirms_2nd_SUI.flush();
            fileSensEnterFirms_2nd_SUI.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensShare_2nd_SUI.flush();
            fileSensShare_2nd_SUI.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensShare_3rd_SUI.flush();
            fileSensShare_3rd_SUI.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensShare_best2nd_SUI.flush();
            fileSensShare_best2nd_SUI.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensShare_1st_LO.flush();
            fileSensShare_1st_LO.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensShare_2nd_LO.flush();
            fileSensShare_2nd_LO.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
        try {
            fileSensParameters.flush();
            fileSensParameters.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    /* This is a method to initialize the output file objects                 */
    void openFile() {
        try {
            fileSensHerf_LO = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensHerf_LO)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensHerf_SUI = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensHerf_SUI)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensEnterFirms_1st_LO = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensEnterFirms_1st_LO)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensEnterFirms_2nd_LO = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensEnterFirms_2nd_LO)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensEnterFirms_3rd_SUI = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensEnterFirms_3rd_SUI)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensEnterFirms_2nd_SUI = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensEnterFirms_2nd_SUI)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensShare_2nd_SUI = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensShare_2nd_SUI)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensShare_3rd_SUI = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensShare_3rd_SUI)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensShare_best2nd_SUI = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensShare_best2nd_SUI)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensShare_1st_LO = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensShare_1st_LO)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensShare_2nd_LO = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensShare_2nd_LO)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensParameters = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensParameters)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    /* The following are ancillary methods to write data in the output file   *
     * objects                                                                */
    void printSensHerf_LO(String str) {
        try {
            fileSensHerf_LO.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensHerf_SUI(String str) {
        try {
            fileSensHerf_SUI.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensEnterFirms_1st_LO(String str) {
        try {
            fileSensEnterFirms_1st_LO.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensEnterFirms_2nd_LO(String str) {
        try {
            fileSensEnterFirms_2nd_LO.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensEnterFirms_3rd_SUI(String str) {
        try {
            fileSensEnterFirms_3rd_SUI.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensEnterFirms_2nd_SUI(String str) {
        try {
            fileSensEnterFirms_2nd_SUI.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensShare_2nd_SUI(String str) {
        try {
            fileSensShare_2nd_SUI.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensShare_3rd_SUI(String str) {
        try {
            fileSensShare_3rd_SUI.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensShare_best2nd_SUI(String str) {
        try {
            fileSensShare_best2nd_SUI.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensShare_1st_LO(String str) {
        try {
            fileSensShare_1st_LO.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensShare_2nd_LO(String str) {
        try {
            fileSensShare_2nd_LO.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensParameters(String str) {
        try {
            fileSensParameters.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    /* The following are ancillary methods to transfer data from the regular  *
     * statistics object to the sensitivity analysis storage objects          */
    void copyValues(ArrayList input, String[] output) {
        for (int i = 0; i < input.size(); i++) {
            output[i] = input.get(i).toString();
        }
    }
    
    void copyValuesParam(Parameter[] input, String[] output) {
        for (int i = 0; i < input.length; i++) {
            output[i] = input[i].getValue();
        }
    }
    
    /* This method gets data from the current simulation run and stores them  *
     * into the storage objects                                               */
    void makeStatistics() {
    
        sensHerf_LO.add(new String[model.endTime+1]);  
        copyValues(model.stat.herf_LO, sensHerf_LO.get(sensHerf_LO.size()-1));
        sensHerf_SUI.add(new String[model.endTime+1]);
        copyValues(model.stat.herf_SUI, sensHerf_SUI.get(sensHerf_SUI.size()-1));
        sensEnterFirms_1st_LO.add(new String[model.endTime+1]);
        copyValues(model.stat.enterFirms_1st_LO, sensEnterFirms_1st_LO.get(sensEnterFirms_1st_LO.size()-1));
        sensEnterFirms_2nd_LO.add(new String[model.endTime+1]);
        copyValues(model.stat.enterFirms_2nd_LO, sensEnterFirms_2nd_LO.get(sensEnterFirms_2nd_LO.size()-1));
        sensEnterFirms_3rd_SUI.add(new String[model.endTime+1]);
        copyValues(model.stat.enterFirms_3rd_SUI, sensEnterFirms_3rd_SUI.get(sensEnterFirms_3rd_SUI.size()-1));
        sensEnterFirms_2nd_SUI.add(new String[model.endTime+1]);
        copyValues(model.stat.enterFirms_2nd_SUI, sensEnterFirms_2nd_SUI.get(sensEnterFirms_2nd_SUI.size()-1));
        sensShare_2nd_SUI.add(new String[model.endTime+1]);
        copyValues(model.stat.share_2nd_SUI, sensShare_2nd_SUI.get(sensShare_2nd_SUI.size()-1));
        sensShare_3rd_SUI.add(new String[model.endTime+1]);
        copyValues(model.stat.share_3rd_SUI, sensShare_3rd_SUI.get(sensShare_3rd_SUI.size()-1));
        sensShare_best2nd_SUI.add(new String[model.endTime+1]);
        copyValues(model.stat.share_best2nd_SUI, sensShare_best2nd_SUI.get(sensShare_best2nd_SUI.size()-1));
        sensShare_1st_LO.add(new String[model.endTime+1]);
        copyValues(model.stat.share_1st_LO, sensShare_1st_LO.get(sensShare_1st_LO.size()-1));
        sensShare_2nd_LO.add(new String[model.endTime+1]);
        copyValues(model.stat.share_2nd_LO, sensShare_2nd_LO.get(sensShare_2nd_LO.size()-1));
        sensParameters.add(new String[200]);
        copyValuesParam(model.parameters, sensParameters.get(sensParameters.size()-1));
    }

    /* This method writes data in the output file in case of sensitivity      *
     * analysis                                                               */
    void printStatistics() {

        for (int i = 0; i < sensHerf_LO.size(); i++) {
            printSensHerf_LO(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensHerf_LO(sensHerf_LO.get(i)[t]+";");
            }
            printSensHerf_LO("\n");
        }
        
        for (int i = 0; i < sensHerf_SUI.size(); i++) {
            printSensHerf_SUI(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensHerf_SUI(sensHerf_SUI.get(i)[t]+";");
            }
            printSensHerf_SUI("\n");
        }
        
        for (int i = 0; i < sensEnterFirms_1st_LO.size(); i++) {
            printSensEnterFirms_1st_LO(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensEnterFirms_1st_LO(sensEnterFirms_1st_LO.get(i)[t]+";");
            }
            printSensEnterFirms_1st_LO("\n");
        }
        
        for (int i = 0; i < sensEnterFirms_2nd_LO.size(); i++) {
            printSensEnterFirms_2nd_LO(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensEnterFirms_2nd_LO(sensEnterFirms_2nd_LO.get(i)[t]+";");
            }
            printSensEnterFirms_2nd_LO("\n");
        }
        
        for (int i = 0; i < sensEnterFirms_3rd_SUI.size(); i++) {
            printSensEnterFirms_3rd_SUI(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensEnterFirms_3rd_SUI(sensEnterFirms_3rd_SUI.get(i)[t]+";");
            }
            printSensEnterFirms_3rd_SUI("\n");
        }
        
        for (int i = 0; i < sensEnterFirms_2nd_SUI.size(); i++) {
            printSensEnterFirms_2nd_SUI(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensEnterFirms_2nd_SUI(sensEnterFirms_2nd_SUI.get(i)[t]+";");
            }
            printSensEnterFirms_2nd_SUI("\n");
        }
        
        for (int i = 0; i < sensShare_2nd_SUI.size(); i++) {
            printSensShare_2nd_SUI(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensShare_2nd_SUI(sensShare_2nd_SUI.get(i)[t]+";");
            }
            printSensShare_2nd_SUI("\n");
        }
        
        for (int i = 0; i < sensShare_3rd_SUI.size(); i++) {
            printSensShare_3rd_SUI(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensShare_3rd_SUI(sensShare_3rd_SUI.get(i)[t]+";");
            }
            printSensShare_3rd_SUI("\n");
        }
        
        for (int i = 0; i < sensShare_best2nd_SUI.size(); i++) {
            printSensShare_best2nd_SUI(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensShare_best2nd_SUI(sensShare_best2nd_SUI.get(i)[t]+";");
            }
            printSensShare_best2nd_SUI("\n");
        }
        
        for (int i = 0; i < sensShare_1st_LO.size(); i++) {
            printSensShare_1st_LO(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensShare_1st_LO(sensShare_1st_LO.get(i)[t]+";");
            }
            printSensShare_1st_LO("\n");
        }
        
        for (int i = 0; i < sensShare_2nd_LO.size(); i++) {
            printSensShare_2nd_LO(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensShare_2nd_LO(sensShare_2nd_LO.get(i)[t]+";");
            }
            printSensShare_2nd_LO("\n");
        }
        
        for (int i = 0; i < sensParameters.size(); i++) {
            printSensParameters(i+";");
            for (int t = 1; t < sensParameters.get(i).length; t++) {
                printSensParameters(sensParameters.get(i)[t] +";");
            }
            printSensParameters("\n");
        }
    }
    
}