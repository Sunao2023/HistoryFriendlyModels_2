package Chapter3;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Random;

/*                                                                            *
 * The US computer industry and the dynamics of concentration:                *
 * Simulation code                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This is the main class of the model described in Chapter 3. Here           *
 * parameters are uploaded using the method importParameters and the timeline *
 * of the model is represented in the method makeSingleSimulation             */
public class C3Model {

    // TECHNICAL VARIABLES & OBJECTS
    String pathParameters;
    /* String containing the path where input file is located                 */
    String pathResults;
    /* String containing the path where output files are saved                */
    Random RNG;
    /* Random number generator                                                */
    Parameter[] parameters;
    /* Array containing all information about the parameters                  */
    String[] paramIN;
    /* Array containing parameters about the industry supply side             */
    String[] paramTR;
    /* Array containing parameters about the transistor technology            */
    String[] paramMP;
    /* Array containing parameters about the microprocessor technology        */
    String[] paramCD;
    /* Array containing common parameters about the demand side               */
    String[] paramLO;
    /* Array containing common parameters about the large organiations user   *
     * class                                                                  */
    String[] paramSUI;
    /* Array containing common parameters about the small users and           *
     * individuals user class                                                 */
    Statistics stat;
    /* Object to store and print relevant statistics                          */
    SA_Statistics sens;
    /* Object to store and print relevant statistics for sensitivity analysis */
    Technology TR_TEC;
    /* Transistor (TR) technology                                             */
    Technology MP_TEC;
    /* Microprocessor (MP) technology                                         */
    Industry  computerIndustry;
    /* Supply side of computer industry                                       */
    UserClass largeOrgs;
    /* Large organizations (LO) user class                                    */
    UserClass smallUsers;
    /* Small users and individuals (SUI) user class                           */
    
    // PARAMETERS
    int endTime;
    /* Periods of simulation (T)                                              */
    int multiTime;
    /* Number of runs under each parameter combination                        */
    int multiSens;
    /* Number of randomly extracted parameter combinations for sensitivity    *
     * analysis                                                               */
    int entryTime_MP;
    /* Period of entry of microprocessor-based firms (T-AD)                   */
    int introTime_MP;
    /* Period from which microprocessors can be adoopted by computer firms    *
     * (T_MP)                                                                 */
    double awareDiv;
    /* Minimum threshold for diversification in the PC market (lambda-DV)     */
    
    // VARIABLES
    int timer;
    /* Time indicator (t)                                                     */
    
    // CONSTRUCTOR
    public C3Model() {
        
        String mainPath = new File("").getAbsolutePath();
        String subPath  = this.getClass().getName().substring(0, this.getClass().getName().indexOf("."));
        pathParameters  = mainPath+"/parameters/"+subPath+"/parameters.txt";
        pathResults     = mainPath+"/results/"+subPath;
        RNG             = new Random(13);
        /* This is the random number generator for all random numbers of the  *
         * model. To reproduce the figures of the book, use 13 as seed.       *
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
            int startIN  = 0, endIN  = 0;
            int startTR  = 0, endTR  = 0;
            int startMP  = 0, endMP  = 0;
            int startCD  = 0, endCD  = 0;
            int startLO  = 0, endLO  = 0;
            int startSUI = 0, endSUI = 0;
            
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
                            parameters[nn].setIsUnderSA(Boolean.valueOf(true));
                            parameters[nn].setConversionType(line.substring(cType + 1, line.length()));
                        }
                        else {
                            parameters[nn].setValue(line.substring(line.indexOf("=") + 2, line.length()));
                        }
                        parameters[nn].setName(line.substring(0, line.indexOf("=") - 1));
                        if (parameters[nn].getName().contains("--IN-S-")) {
                            startIN = nn + 1;
                        }
                        if (parameters[nn].getName().contains("--IN-E-")) {
                            endIN = nn - 1;
                        }
                        if (parameters[nn].getName().contains("--TR-S-")) {
                            startTR = nn + 1;
                        }
                        if (parameters[nn].getName().contains("--TR-E-")) {
                            endTR = nn - 1;
                        }
                        if (parameters[nn].getName().contains("--MP-S-")) {
                            startMP = nn + 1;
                        }
                        if (parameters[nn].getName().contains("--MP-E-")) {
                            endMP = nn - 1;
                        }
                        if (parameters[nn].getName().contains("--CD-S-")) {
                            startCD = nn + 1;
                        }
                        if (parameters[nn].getName().contains("--CD-E-")) {
                            endCD = nn - 1;
                        }
                        if (parameters[nn].getName().contains("--LO-S-")) {
                            startLO = nn + 1;
                        }
                        if (parameters[nn].getName().contains("--LO-E-")) {
                            endLO = nn - 1;
                        }
                        if (parameters[nn].getName().contains("--SUI-S-")) {
                            startSUI = nn + 1;
                        }
                        if (parameters[nn].getName().contains("--SUI-E-")) {
                            endSUI = nn - 1;
                        }
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
            
            paramIN = new String[endIN - startIN + 2];
            paramTR = new String[endTR - startTR + 2];
            paramMP = new String[endMP - startMP + 2];
            paramCD = new String[endCD - startCD + 2];
            paramLO = new String[endLO - startLO + 2];
            paramSUI = new String[endSUI - startSUI + 2];
            for (int i = startIN; i <= endIN; i++) {
                paramIN[i - startIN + 1] = parameters[i].getValue();
            }
            for (int i = startTR; i <= endTR; i++) {
                paramTR[i - startTR + 1] = parameters[i].getValue();
            }
            for (int i = startMP; i <= endMP; i++) {
                paramMP[i - startMP + 1] = parameters[i].getValue();
            }
            for (int i = startCD; i <= endCD; i++) {
                paramCD[i - startCD + 1] = parameters[i].getValue();
            }
            for (int i = startLO; i <= endLO; i++) {
                paramLO[i - startLO + 1] = parameters[i].getValue();
            }
            for (int i = startSUI; i <= endSUI; i++) {
                paramSUI[i - startSUI + 1] = parameters[i].getValue();
            }
        }
        
        endTime       = Integer.parseInt(parameters[1].getValue());
        multiTime     = Integer.parseInt(parameters[2].getValue());
        multiSens     = Integer.parseInt(parameters[3].getValue());
        entryTime_MP  = Integer.parseInt(parameters[4].getValue());
        introTime_MP  = Integer.parseInt(parameters[5].getValue());
        awareDiv      = Double.parseDouble(parameters[6].getValue());
        
        largeOrgs  =  new UserClass(paramCD, paramLO, RNG);
        smallUsers =  new UserClass(paramCD, paramSUI, RNG);
        
        TR_TEC = new Technology(paramTR);
        MP_TEC = new Technology(paramMP);
        
        computerIndustry = new Industry(paramIN, TR_TEC, RNG);
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
            if (timer == entryTime_MP) {
                computerIndustry.secondGenerationCreation(timer, MP_TEC);
            }
            if (smallUsers.size > 0) {
                if (smallUsers.size / largeOrgs.size > awareDiv) {
                    computerIndustry.diversification(timer, MP_TEC, smallUsers, largeOrgs);
                }
            }
            computerIndustry.rdInvest(timer);
            computerIndustry.mktingInvest(timer);
            
            if (timer > introTime_MP) {
                computerIndustry.adoption(MP_TEC);
            }
            
            computerIndustry.innovation();
            
            smallUsers.market(computerIndustry, timer);
            largeOrgs.market(computerIndustry, timer);
            
            computerIndustry.accounting(timer);
            
            if(isSingle) {
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