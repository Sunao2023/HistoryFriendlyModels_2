package Chapter4;

import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;

/**
 *
 * @author Gianluca
 */

/* This class contains all elements to store and produce the relevant         *
 * statistics from the simulation model in the case of sensitivity analysis   */
class SA_Statistics{

    // TECHNICAL VARIABLES AND OBJECTS
    C4Model model;
    /* Access to simulation data                                              */
    DataOutputStream fileSensAliveFirms_MF;
    /* Output file of number of active firms in Mainframes market             */
    String           nameSensAliveFirms_MF;
    /* Name of the output file of number of active firms in Mainframes market */
    DataOutputStream fileSensAliveFirms_PC;
    /* Output file of number of active firms in PC market                     */
    String           nameSensAliveFirms_PC;
    /* Name of the output file of number of active firms in PC market         */
    DataOutputStream fileSensAliveFirms_CMP;
    /* Output file of number of active firms in Component market              */
    String           nameSensAliveFirms_CMP;
    /* Name of the output file of number of active firms in Component market  */
    DataOutputStream fileSensHerf_MF;
    /* Output file of herfindahl in Mainframes market                         */
    String           nameSensHerf_MF;
    /* Name of the output file of herfindahl in Mainframes market             */
    DataOutputStream fileSensHerf_PC;
    /* Output file of herfindahl in PC market                                 */
    String           nameSensHerf_PC;
    /* Name of the output file of herfindahl in PC market                     */
    DataOutputStream fileSensHerf_CMP;
    /* Output file of herfindahl in Component market                          */
    String           nameSensHerf_CMP;
    /* Name of the output file of herfindahl in Component market              */
    DataOutputStream fileSensIntRatio_MF;
    /* Output file of integration ratio in Mainframes market                  */
    String           nameSensIntRatio_MF;
    /* Name of the output file of integration ratio in Mainframes market      */
    DataOutputStream fileSensIntRatio_PC;
    /* Output file of integration ratio in PC market                          */
    String           nameSensIntRatio_PC;
    /*Name of the output file of integration ratio in PC market               */
    DataOutputStream fileSensParameters;
    /* Output file object of parameters                                       */
    String           nameSensParameters;
    /* Name of the output file of parameters                                  */
    
    // STATS VARIABLES
    ArrayList<String[]> sensAliveFirms_MF;
    /* Storage of number of active firms in Mainframes market                 */
    ArrayList<String[]> sensAliveFirms_PC;
    /* Storage of number of active firms in PC market                         */
    ArrayList<String[]> sensAliveFirms_CMP;
    /* Storage of number of active firms in Component market                  */
    ArrayList<String[]> sensHerf_MF;
    /* Storage of herfindahl index in Mainframes market                       */
    ArrayList<String[]> sensHerf_PC;
    /* Storage of herfindahl index in PC market                               */
    ArrayList<String[]> sensHerf_CMP;
    /* Storage of herfindahl index in Component market                        */
    ArrayList<String[]> sensIntRatio_MF;
    /* Storage of integration ratio in Mainframes market                      */
    ArrayList<String[]> sensIntRatio_PC;
    /* Storage of integration ratio in PC market                              */
    ArrayList<String[]> sensParameters;
    /* Storage of parameters used in the simulation runs                      */
    
    // CONSTRUCTOR
    SA_Statistics(C4Model MODEL) {
        
        model                 = MODEL;
        
        nameSensHerf_MF        = "/sa_herf_MF.csv";
        nameSensHerf_PC        = "/sa_herf_PC.csv";
        nameSensHerf_CMP       = "/sa_herf_CMP.csv";
        nameSensAliveFirms_MF  = "/sa_firms_MF.csv";
        nameSensAliveFirms_PC  = "/sa_firms_PC.csv";
        nameSensAliveFirms_CMP = "/sa_firms_CMP.csv";
        nameSensIntRatio_MF    = "/sa_intRat_MF.csv";
        nameSensIntRatio_PC    = "/sa_intRat_PC.csv";
        nameSensParameters     = "/sa_parameters.csv";
        
        sensHerf_MF        = new ArrayList<String[]>();
        sensHerf_PC        = new ArrayList<String[]>();
        sensHerf_CMP       = new ArrayList<String[]>();
        sensAliveFirms_MF  = new ArrayList<String[]>();
        sensAliveFirms_PC  = new ArrayList<String[]>();
        sensAliveFirms_CMP = new ArrayList<String[]>();
        sensIntRatio_MF    = new ArrayList<String[]>();
        sensIntRatio_PC    = new ArrayList<String[]>();
        sensParameters     = new ArrayList<String[]>();
    }
    
    /* This is a method to close the output file objects                      */
    public void closeFile() {
        try {
            fileSensHerf_MF.flush();
            fileSensHerf_MF.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensHerf_PC.flush();
            fileSensHerf_PC.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensHerf_CMP.flush();
            fileSensHerf_CMP.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensAliveFirms_MF.flush();
            fileSensAliveFirms_MF.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensAliveFirms_PC.flush();
            fileSensAliveFirms_PC.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensAliveFirms_CMP.flush();
            fileSensAliveFirms_CMP.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensIntRatio_MF.flush();
            fileSensIntRatio_MF.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensIntRatio_PC.flush();
            fileSensIntRatio_PC.close();
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
            fileSensHerf_MF = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensHerf_MF)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensHerf_PC = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensHerf_PC)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensHerf_CMP = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensHerf_CMP)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensAliveFirms_MF = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensAliveFirms_MF)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensAliveFirms_PC = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensAliveFirms_PC)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensAliveFirms_CMP = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensAliveFirms_CMP)));
        } catch(IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensIntRatio_MF = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensIntRatio_MF)));
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        try {
            fileSensIntRatio_PC = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(model.pathResults+nameSensIntRatio_PC)));
        } catch(IOException e) {
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
    void printSensHerf_MF(String str) {
        try {
            fileSensHerf_MF.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensHerf_PC(String str) {
        try {
            fileSensHerf_PC.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensHerf_CMP(String str) {
        try {
            fileSensHerf_CMP.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensAliveFirms_MF(String str) {
        try {
            fileSensAliveFirms_MF.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensAliveFirms_PC(String str) {
        try {
            fileSensAliveFirms_PC.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensAliveFirms_CMP(String str) {
        try {
            fileSensAliveFirms_CMP.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensIntRatio_MF(String str) {
        try {
            fileSensIntRatio_MF.writeBytes(str);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
    void printSensIntRatio_PC(String str) {
        try {
            fileSensIntRatio_PC.writeBytes(str);
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
    
        sensHerf_MF.add(new String[model.endTime+1]);  
        copyValues(model.stat.herf_MF, sensHerf_MF.get(sensHerf_MF.size()-1));
        sensHerf_PC.add(new String[model.endTime+1]);
        copyValues(model.stat.herf_PC, sensHerf_PC.get(sensHerf_PC.size()-1));
        sensHerf_CMP.add(new String[model.endTime+1]);
        copyValues(model.stat.herf_CMP, sensHerf_CMP.get(sensHerf_CMP.size()-1));
        sensAliveFirms_MF.add(new String[model.endTime+1]);
        copyValues(model.stat.aliveFirms_MF, sensAliveFirms_MF.get(sensAliveFirms_MF.size()-1));
        sensAliveFirms_PC.add(new String[model.endTime+1]);
        copyValues(model.stat.aliveFirms_PC, sensAliveFirms_PC.get(sensAliveFirms_PC.size()-1));
        sensAliveFirms_CMP.add(new String[model.endTime+1]);
        copyValues(model.stat.aliveFirms_CMP, sensAliveFirms_CMP.get(sensAliveFirms_CMP.size()-1));
        sensIntRatio_MF.add(new String[model.endTime+1]);
        copyValues(model.stat.intRatio_MF, sensIntRatio_MF.get(sensIntRatio_MF.size()-1));
        sensIntRatio_PC.add(new String[model.endTime+1]);
        copyValues(model.stat.intRatio_PC, sensIntRatio_PC.get(sensIntRatio_PC.size()-1));
        sensParameters.add(new String[200]);
        copyValuesParam(model.parameters, sensParameters.get(sensParameters.size()-1));
    }
    
    /* This method writes data in the output file in case of sensitivity      *
     * analysis                                                               */
    void printStatistics() {

        for (int i = 0; i < sensHerf_MF.size(); i++) {
            printSensHerf_MF(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensHerf_MF(sensHerf_MF.get(i)[t]+";");
            }
            printSensHerf_MF("\n");
        }
        
        for (int i = 0; i < sensHerf_PC.size(); i++) {
            printSensHerf_PC(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensHerf_PC(sensHerf_PC.get(i)[t]+";");
            }
            printSensHerf_PC("\n");
        }
        
        for (int i = 0; i < sensHerf_CMP.size(); i++) {
            printSensHerf_CMP(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensHerf_CMP(sensHerf_CMP.get(i)[t]+";");
            }
            printSensHerf_CMP("\n");
        }
        
        for (int i = 0; i < sensAliveFirms_MF.size(); i++) {
            printSensAliveFirms_MF(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensAliveFirms_MF(sensAliveFirms_MF.get(i)[t]+";");
            }
            printSensAliveFirms_MF("\n");
        }
        
        for (int i = 0; i < sensAliveFirms_PC.size(); i++) {
            printSensAliveFirms_PC(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensAliveFirms_PC(sensAliveFirms_PC.get(i)[t]+";");
            }
            printSensAliveFirms_PC("\n");
        }
        
        for (int i = 0; i < sensAliveFirms_CMP.size(); i++) {
            printSensAliveFirms_CMP(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensAliveFirms_CMP(sensAliveFirms_CMP.get(i)[t]+";");
            }
            printSensAliveFirms_CMP("\n");
        }
        
        for (int i = 0; i < sensIntRatio_MF.size(); i++) {
            printSensIntRatio_MF(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensIntRatio_MF(sensIntRatio_MF.get(i)[t]+";");
            }
            printSensIntRatio_MF("\n");
        }
        
        for (int i = 0; i < sensIntRatio_PC.size(); i++) {
            printSensIntRatio_PC(i+";");
            for (int t = 1; t <= model.endTime; t++) {
                printSensIntRatio_PC(sensIntRatio_PC.get(i)[t]+";");
            }
            printSensIntRatio_PC("\n");
        }
        
        for (int i = 0; i < sensParameters.size(); i++) {
            printSensParameters(i+";");
            for (int j = 1; j < sensParameters.get(i).length; j++) {
                printSensParameters(sensParameters.get(i)[j] +";");
            }
            printSensParameters("\n");
        }
    }
}
