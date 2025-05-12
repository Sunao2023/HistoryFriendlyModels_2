package Chapter4;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Random;

/*                                                                            *
 * Vertical integration and dis-integration in the computer industry:         *
 * Simulation code                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This is the main class of the model described in Chapter 4. Here           *
 * parameters are uploaded using the method importParameters and the timeline *
 * of the model is represented in the method makeSingleSimulation             */
public class C4Model {
    
    // TECHNICAL VARIABLES & OBJECTS
    String pathParameters;
    /* String containing the path where input file is located                 */
    String pathResults;
    /* String containing the path where output files are saved                */
    Random RNG;
    /* Random number generator                                                */
    Parameter[] parameters;
    /* Array containing all information about the parameters                  */
    Statistics stat;
    /* Object to store and print relevant statistics                          */
    SA_Statistics sens;
    /* Object to store and print relevant statistics for sensitivity analysis */
    ComponentMarket CmpMarket;
    /* Component market                                                       */
    ComputerMarket  MFMarket;
    /* Mainframes market                                                      */
    ComputerMarket  PCMarket;
    /* Personal Computers (PC) market                                         */

    // PARAMETERS
    int endTime;
    /* Periods of simulation (T)                                              */
    int multiTime;
    /* Number of runs under each parameter combination                        */
    int multiSens;
    /* Number of randomly extracted parameter combinations for sensitivity    *
     * analysis                                                               */
    int[] entryTime_CMP = new int[3];
    /* Periods of entry of specialized component firms (T_k)                  */
    int entryTime_PC;
    /* Period of entry of PC firms (T_PC)                                     */
    int numOfFirm_MF;
    /* Number of firms entering the Mainframes market (F_MF)                  */
    int numOfFirm_PC;
    /* Number of firms entering the PC market (F_PC)                          */
    int numOfFirm_CMP;
    /* Number of firms entering the Component market when a new technology    *
     * emerges (F_k)                                                          */
    
    // VARIABLES
    boolean PCentry;
    /* Controller of emergence of PC market                                   */
    int timer;
    /* Time indicator (t)                                                     */
    
    // CONSTRUCTOR
    public C4Model() {
        
        String mainPath = new File("").getAbsolutePath();
        String subPath  = this.getClass().getName().substring(0, this.getClass().getName().indexOf("."));
        pathParameters  = mainPath+"/parameters/"+subPath+"/parameters.txt";
        pathResults     = mainPath+"/results/"+subPath;        
        RNG             = new Random(1000);
        /* This is the random number generator for all random numbers of the  *
         * model. To reproduce the figures of the book, use 1000 as seed.     *
         * Remove the seed to get different results.                          */
        parameters      = new Parameter[200];
    }

    /* This method is used to import parameters from a txt file, to store     *
     * them into suitable objects, and to initalize the main objects of the   *
     * model. The control reloadParam takes value "TRUE" whenever it is       *
     * necessary to use a new set of parameters. The control isSens takes     *
     * value "TRUE" when parameters subject to sensitivity analysis must be   *
     * randomly extracted                                                     */
    void importParameters(boolean isSens, boolean reloadParam) {
        
        if (reloadParam) {
            for (int i = 0; i < 200; i++) {
                parameters[i] = new Parameter();
            }
            
            String line;
            int nn = 1;        
            
            try {
                BufferedReader input = new BufferedReader(new FileReader(pathParameters));

                do {
                    line = input.readLine();
                    if (line != null) {
                        int isUnderSA = line.indexOf('@');
                        if (isUnderSA > 0) {
                            parameters[nn].setValue(line.substring(line.indexOf("=") + 2, isUnderSA));                        
                            int cType = line.indexOf('§');
                            parameters[nn].setVariation(line.substring(isUnderSA + 1, cType));
                            parameters[nn].setIsUnderSA(true);
                            parameters[nn].setConversionType(line.substring(cType + 1, line.length()));
                        }
                        else {
                            parameters[nn].setValue(line.substring(line.indexOf("=") + 2, line.length()));
                        }   
                        parameters[nn].setName(line.substring(0, line.indexOf("=") - 1));
                        nn++;
                    }
                }
                while (line != null);
            }
            catch (IOException e) {
                System.out.println(e.getMessage());
            }

            parameters[0].setValue(String.valueOf(nn - 1));
            if (isSens) {
                checkParamValueForSA();
            }
        }
        
        /* Iterations / Sensitivity                                           */
        multiTime = Integer.parseInt(parameters[1].getValue());
        multiSens = Integer.parseInt(parameters[3].getValue()); 
        
        /* All industries: timing and entry                                   */
        endTime          = Integer.parseInt(parameters[2].getValue());
        numOfFirm_CMP    = Integer.parseInt(parameters[4].getValue());
        numOfFirm_MF     = Integer.parseInt(parameters[5].getValue());
        numOfFirm_PC     = Integer.parseInt(parameters[6].getValue());
        entryTime_CMP[0] = Integer.parseInt(parameters[7].getValue());
        entryTime_CMP[1] = Integer.parseInt(parameters[8].getValue());
        entryTime_CMP[2] = Integer.parseInt(parameters[9].getValue());
        int entryTime_MF = Integer.parseInt(parameters[62].getValue());
        entryTime_PC     = Integer.parseInt(parameters[10].getValue());
        PCentry          = Boolean.valueOf(parameters[86].getValue()).booleanValue();
        
        /* All industries: Common Elements                                    */
        double internalCum = Double.parseDouble(parameters[61].getValue());
        double markup      = Double.parseDouble(parameters[32].getValue());
        double rdOnProf    = Double.parseDouble(parameters[31].getValue());
        
        /* Components: Demand / Market                                        */
        double deltaMod_CMP     = Double.parseDouble(parameters[43].getValue());
        double[] deltaShare_CMP = new double[3];
        deltaShare_CMP[0]       = Double.parseDouble(parameters[46].getValue());
        deltaShare_CMP[1]       = Double.parseDouble(parameters[47].getValue());
        deltaShare_CMP[2]       = Double.parseDouble(parameters[48].getValue());
        int[] externalMkts_CMP  = new int[3];
        externalMkts_CMP[0]     = Integer.parseInt(parameters[13].getValue());
        externalMkts_CMP[1]     = Integer.parseInt(parameters[14].getValue());
        externalMkts_CMP[2]     = Integer.parseInt(parameters[15].getValue());
        int buyers_CMP          = numOfFirm_MF + numOfFirm_PC;
        int exitThreshold_CMP   = Integer.parseInt(parameters[87].getValue());
        
        /* Components: Technology                                             */
        double[] drawCost_CMP = new double[3];
        drawCost_CMP[0]       = Double.parseDouble(parameters[51].getValue());
        drawCost_CMP[1]       = Double.parseDouble(parameters[52].getValue());
        drawCost_CMP[2]       = Double.parseDouble(parameters[53].getValue());
        int entDel_CMP        = Integer.parseInt(parameters[89].getValue());
        double[] l1_CMP       = new double[3];
        l1_CMP[0]             = Double.parseDouble(parameters[66].getValue());
        l1_CMP[1]             = Double.parseDouble(parameters[67].getValue());
        l1_CMP[2]             = Double.parseDouble(parameters[68].getValue());
        double[] l2_CMP       = new double[3];
        l2_CMP[0]             = Double.parseDouble(parameters[71].getValue());
        l2_CMP[1]             = Double.parseDouble(parameters[72].getValue());
        l2_CMP[2]             = Double.parseDouble(parameters[73].getValue());
        double[] l0_CMP       = new double[3];
        l0_CMP[0]             = Double.parseDouble(parameters[63].getValue());
        l0_CMP[1]             = (l0_CMP[0] * Math.exp(l1_CMP[0] * entryTime_CMP[1])
                                 * (1 - 1 / (l2_CMP[0] * (entryTime_CMP[1]
                                    - (entryTime_CMP[0] - entDel_CMP)))))
                              / (Math.exp(l1_CMP[1] * entryTime_CMP[1])
                                 * (1 - 1 / (l2_CMP[1] * entDel_CMP)));
        l0_CMP[2]             = (l0_CMP[1] * Math.exp(l1_CMP[1] * entryTime_CMP[2])
                                 * (1 - 1 / (l2_CMP[1] * (entryTime_CMP[2]
                                    - (entryTime_CMP[1] - entDel_CMP)))))
                              / (Math.exp(l1_CMP[2] * entryTime_CMP[2])
                                 * (1 - 1 / (l2_CMP[2] * entDel_CMP)));
        double nu_CMP         = Double.parseDouble(parameters[28].getValue());
        double[] startMod_CMP = new double[3];
        startMod_CMP[0]       = Double.parseDouble(parameters[20].getValue());
        startMod_CMP[1]       = Double.parseDouble(parameters[21].getValue());
        startMod_CMP[2]       = Double.parseDouble(parameters[22].getValue());
        double[] stDev_CMP    = new double[3];
        stDev_CMP[0]          = Double.parseDouble(parameters[56].getValue());
        stDev_CMP[1]          = Double.parseDouble(parameters[57].getValue());
        stDev_CMP[2]          = Double.parseDouble(parameters[58].getValue());
        
        CmpMarket = new ComponentMarket(numOfFirm_CMP, deltaMod_CMP, deltaShare_CMP,
                         nu_CMP, rdOnProf, markup, internalCum, stDev_CMP,
                         drawCost_CMP, startMod_CMP, l0_CMP, l1_CMP, l2_CMP,
                         externalMkts_CMP, buyers_CMP, exitThreshold_CMP,
                         entryTime_CMP, entDel_CMP, RNG);
        
        /* Computers: Common Elements                                         */
        double chi0         = Double.parseDouble(parameters[80].getValue());
        double chi1         = Double.parseDouble(parameters[78].getValue());
        double chi2         = Double.parseDouble(parameters[79].getValue());
        int entDel_SYS      = Integer.parseInt(parameters[88].getValue());
        double exitSharePar = Double.parseDouble(parameters[84].getValue());
        double inherMod     = Double.parseDouble(parameters[82].getValue());
        int lengContMin     = Integer.parseInt(parameters[11].getValue());
        int lengContBias    = Integer.parseInt(parameters[12].getValue());
        double[] maxMod_SYS = new double[3];
        maxMod_SYS[0]       = Double.parseDouble(parameters[25].getValue());
        maxMod_SYS[1]       = Double.parseDouble(parameters[26].getValue());
        maxMod_SYS[2]       = Double.parseDouble(parameters[27].getValue());
        int minIntTime      = Integer.parseInt(parameters[76].getValue());
        double spillover    = Double.parseDouble(parameters[81].getValue());
        double weightExit   = Double.parseDouble(parameters[85].getValue());
        double xiInt        = Double.parseDouble(parameters[77].getValue());
        double xiSpec       = Double.parseDouble(parameters[83].getValue());
                
        /* Mainframes: Demand / Market                                        */
        int buyers_MF           = Integer.parseInt(parameters[16].getValue());
        double deltaMod_MF      = Double.parseDouble(parameters[44].getValue());
        double deltaShare_MF    = Double.parseDouble(parameters[49].getValue());
        double gamma_MF         = Double.parseDouble(parameters[41].getValue());
        double startShare_MF    = (1 / (double) numOfFirm_MF);
        double exitThreshold_MF = exitSharePar * startShare_MF;
        
        /* Mainframes: Technology                                             */
        double drawCost_MF    = Double.parseDouble(parameters[54].getValue());
        double l0_MF          = Double.parseDouble(parameters[64].getValue());
        double l1_MF          = Double.parseDouble(parameters[69].getValue());
        double l2_MF          = Double.parseDouble(parameters[74].getValue());
        double nu_MF          = Double.parseDouble(parameters[29].getValue());
        double numOfCmp_MF    = Double.parseDouble(parameters[18].getValue());
        double phi_MF         = Double.parseDouble(parameters[33].getValue());
        double ro_MF          = Double.parseDouble(parameters[37].getValue());
        double startModSys_MF = Double.parseDouble(parameters[23].getValue());
        double tau_MF         = Double.parseDouble(parameters[35].getValue());
        double tempAngle_MF   = Double.parseDouble(parameters[39].getValue());
        double theta_MF       = Math.PI / tempAngle_MF;
        double stDev_MF       = Double.parseDouble(parameters[59].getValue());
        
        MFMarket = new ComputerMarket("MF", numOfFirm_MF, buyers_MF, deltaMod_MF,
                        deltaShare_MF, nu_MF, nu_CMP, false, rdOnProf, markup,
                        startShare_MF, spillover, numOfCmp_MF, ro_MF, tau_MF,
                        phi_MF, startModSys_MF, internalCum, lengContMin,
                        lengContBias, xiInt, chi1, chi2, chi0, xiSpec, minIntTime,
                        inherMod, entryTime_CMP, maxMod_SYS, entDel_SYS, entDel_CMP,
                        theta_MF, gamma_MF, stDev_MF, stDev_CMP, l0_CMP, l1_CMP,
                        l2_CMP, l0_MF, l1_MF, l2_MF, drawCost_MF, drawCost_CMP,
                        entryTime_MF, weightExit, exitThreshold_MF, RNG);
        
        /* PCs: Demand / Market                                               */
        int buyers_PC           = Integer.parseInt(parameters[17].getValue());
        double deltaMod_PC      = Double.parseDouble(parameters[45].getValue());
        double deltaShare_PC    = Double.parseDouble(parameters[50].getValue());
        double gamma_PC         = Double.parseDouble(parameters[42].getValue());
        double startShare_PC    = (1 / (double) numOfFirm_PC);
        double exitThreshold_PC = exitSharePar * startShare_PC;
        
        /* PCs: Technology                                                    */
        double drawCost_PC    = Double.parseDouble(parameters[55].getValue());
        double l0_PC          = Double.parseDouble(parameters[65].getValue());
        double l1_PC          = Double.parseDouble(parameters[70].getValue());
        double l2_PC          = Double.parseDouble(parameters[75].getValue());
        double nu_PC          = Double.parseDouble(parameters[30].getValue());
        double numOfCmp_PC    = Double.parseDouble(parameters[19].getValue());
        double phi_PC         = Double.parseDouble(parameters[34].getValue());
        double ro_PC          = Double.parseDouble(parameters[38].getValue());
        double startModSys_PC = Double.parseDouble(parameters[24].getValue());
        double tau_PC         = Double.parseDouble(parameters[36].getValue());
        double tempAngle_PC   = Double.parseDouble(parameters[40].getValue());
        double theta_PC       = Math.PI / tempAngle_PC;
        double stDev_PC       = Double.parseDouble(parameters[60].getValue());
        
        PCMarket = new ComputerMarket("PC", numOfFirm_PC, buyers_PC, deltaMod_PC,
                        deltaShare_PC, nu_PC, nu_CMP, true, rdOnProf, markup,
                        startShare_PC, spillover, numOfCmp_PC, ro_PC, tau_PC,
                        phi_PC, startModSys_PC, internalCum, lengContMin,
                        lengContBias, xiInt, chi1, chi2, chi0, xiSpec, minIntTime,
                        inherMod, entryTime_CMP, maxMod_SYS, entDel_SYS, entDel_CMP,
                        theta_PC, gamma_PC, stDev_PC, stDev_CMP, l0_CMP, l1_CMP,
                        l2_CMP, l0_PC, l1_PC, l2_PC, drawCost_PC, drawCost_CMP,
                        entryTime_PC, weightExit, exitThreshold_PC, RNG);
    }
    
    /* This is an ancillary method to set parameter values in case of         *
     * sensitivity analsysis extracting them from random distributions        */
    void checkParamValueForSA() {
        for (int i = 1; i <= Integer.parseInt(parameters[0].getValue()); i++) {
            if (parameters[i].getIsUnderSA()) {
                double value = Double.parseDouble(parameters[i].getValue());
                double variation = Double.parseDouble(parameters[i].getVariation());
                double min = value - (value *  variation);
                double max = value + (value *  variation); 
                if ("i".equals(parameters[i].getConversionType())) {
                    int iMin = (int) Math.round(min);
                    int iMax = (int) Math.round(max) + 1;
                    int iValue = iMin + RNG.nextInt(iMax - iMin);
                    parameters[i].setValue(Integer.toString((int) iValue));
                }
                else {
                    value = min + (RNG.nextDouble() * (max - min)); 
                    parameters[i].setValue(Double.toString(value)); 
                }
            }
        }
    }

    /* This method controls the timeline of the model. If the control         *
     * isSingle is "TRUE", specific methods to upload parameters and create   *
     * output are used                                                        */
    public void makeSingleSimulation(boolean isSingle) {
        if (isSingle) {
            importParameters(false, true);
            stat = new Statistics(this, true);
            stat.openFile("/singleSimulation.csv");
        }
        else {
            importParameters(false, false);
        }

        for (timer = 1; timer <= endTime; timer++) {
            if (timer == entryTime_CMP[1]) {
                CmpMarket.newEntry(numOfFirm_CMP, 1);
                MFMarket.changeCmpTechnology(1);
            }

            if (timer == entryTime_CMP[2]) {
                CmpMarket.newEntry(numOfFirm_CMP, 2);
                MFMarket.changeCmpTechnology(2);
            }

            if (timer == entryTime_PC) {
                PCentry = true;
            }

            CmpMarket.rating();
            MFMarket.contractEngine(CmpMarket, timer, 0);
            if (PCentry) {
                PCMarket.contractEngine(CmpMarket, timer, numOfFirm_MF);
            }

            MFMarket.rdExpenditure();
            if (PCentry) {
                PCMarket.rdExpenditure();
            }
            CmpMarket.rdExpenditure();
            
            CmpMarket.modProgress(timer);
            MFMarket.modComponentProgress(timer, CmpMarket);
            MFMarket.modSystemProgress(timer);
            if (PCentry) {
                PCMarket.modComponentProgress(timer, CmpMarket);
                PCMarket.modSystemProgress(timer);
            }
            
            MFMarket.computerModCostPrice();
            if (PCentry) {
                PCMarket.computerModCostPrice();
            }
            
            MFMarket.probOfSelling();
            if (PCentry) {
                PCMarket.probOfSelling();
            }
            CmpMarket.externalMkt();
            
            MFMarket.accounting(timer);
            if (PCentry) {
                PCMarket.accounting(timer);
            }
            CmpMarket.accounting(MFMarket, PCMarket, PCentry);
            
            MFMarket.checkExit(CmpMarket, 0);
            if (PCentry) {
                PCMarket.checkExit(CmpMarket, numOfFirm_MF);
            }
            CmpMarket.checkExit();
            
            MFMarket.statistics(endTime);
            if (PCentry) {
                PCMarket.statistics(endTime);
            }
            CmpMarket.statistics();
            
            if (isSingle) {
                stat.makeSingleStatistics();
            }
            else {
                stat.makeStatistics();
            }
        }

        if (isSingle) {
            stat.printSingleStatistics();
            stat.closeFile();
        }
    }

    /* This method automatizes multiple simulation runs. If the control       *
     * isMulti is "TRUE", specific methods to upload parameters and create    *
     * output are used, and the number of the runs are displayed              */
    public void makeMultipleSimulation(boolean isMulti) {
        
        if (isMulti) {
            importParameters(false, true);
        }
        
        stat = new Statistics(this, false);
        if (isMulti) {
            stat.openFile("/multiSimulation.csv");
        }
        
        for (int multiCounter = 1; multiCounter <= multiTime; multiCounter++) {
            if (isMulti) {
                System.out.print(multiCounter + "\n");
            }
            makeSingleSimulation(false);
        }
        
        if (!isMulti) {
            sens.makeStatistics();
        }
        
        if (isMulti) {
            stat.printMultiStatistics();
            stat.closeFile();
        }
    }
    
    /* This method automatizes sensitivity analysis simulation runs. If the   *
     * control printSensCounter is "TRUE" the number of sensitivity runs      *
     * should be displayed                                                    */
    public void makeSensitivitySimulation(boolean printSensCounter) {
        
        importParameters(true, true);
        sens = new SA_Statistics(this);
        sens.openFile();
        
        for (int sensCounter = 1; sensCounter <= multiSens; sensCounter++) {
            importParameters(true, true);
            makeMultipleSimulation(false);
            if (printSensCounter) {
                System.out.print(String.valueOf(sensCounter) + "\n");
            }
        }

        sens.printStatistics();
        sens.closeFile();
    }
}