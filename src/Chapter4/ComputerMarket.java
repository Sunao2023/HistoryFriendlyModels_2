package Chapter4;

import java.util.Random;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all parameters and variables that refer to the         *
 * Computer Markets (Mainframes and PCs), and the methods that operate over   *
 * these variables or call for firm-level methods                             */
class ComputerMarket {
    
    // PARAMETERS
    int buyers;
    /* Number of groups of potential buyers (G_h)                             */
    double chi0;
    /* Multiplier of technology  age in (Integration) Equation 16 (chi-0)     */
    double chi1;
    /* Exponent of technology  age in (Integration) Equation 16 (chi-1        */
    double chi2;
    /* Exponent of size in (Integration) Equation 16 (chi-2)                  */
    double gamma;
    /* Exponent of cheapness determining perceived mod (gamma_h)              */
    double deltaMod;
    /* Exponent of mod in Equation 2 (delta-M_h)                              */
    double deltaShare;
    /* Exponent of market share in Equation 2 (delta-s_kappa)                 */
    double[] drawCostCmp;
    /* Draw cost for component technology in Equation 13.b (C-RD_k)           */
    double drawCostSys;
    /* Draw cost for system technology in Equation 13.a (C-RD_kappa)          */
    int entryDelaySys;
    /* Delay between component technology emergence and entry time of         *
     * component firms (T-CO)                                                 */
    int entryDelayCmp;
    /* Delay between system technology emergence and entry time of computer   *
     * firms (T-SY)                                                           */
    int[] entryTimeCmpTec;
    /* Entry time of component firms, by component technology (T_k)           */
    int entryTimeSysTec;
    /* Entry time of computer firms, by system technology (T_kappa)           */
    double exitThreshold;
    /* Exit threshold for computer firms (lambda-E)                           */
    double inheritance;
    /* Fraction of last supplier mod inherited by a firm moving to vertical   *
     * integration (phi-I)                                                    */
    double internalCum;
    /* Weight of internal mod in Equation 14 (w-K)                            */
    double[] l0Cmp;
    /* Baseline trajectory of component technology public knowledge in        *
     * Equation 15.b (l-0_k)                                                  */
    double[] l1Cmp;
    /* Asymptotic growth rate of component technology public knowledge in     *
     * Equation 15.b (l-1_k)                                                  */
    double[] l2Cmp;
    /* Speed of approach to asymptotic growth rate of component technology    *
     * public knowledge in Equation 15.b (l-2_k)                              */
    double l0Sys;
    /* Baseline trajectory of system technology public knowledge in           *
     * Equation 15.a (l-0_kappa)                                              */
    double l1Sys;
    /* Asymptotic growth rate of system technology public knowledge in        *
     * Equation 15.a (l-1_kappa)                                              */
    double l2Sys;
    /* Speed of approach to asymptotic growth rate of system technology       *
     * public knowledge in Equation 15.a (l-2_kappa)                          */
    double[] limitSysMod;
    /* System mod technological limits (LAMBDA-SY_k)                          */
    double markup;
    /* Markup (m)                                                             */
    int minIntTime;
    /* Minimum duration of integration (T-I)                                  */
    int minLengthContr;
    /* Minimum duration of a contract with a component supplier (T-CO_f,t)    */
    double nuCmp;
    /* Proportionality factor to compute component production cost from Mod   *
     * (nu_k)                                                                 */
    double nuComputer;
    /* Proportionality factor to compute computer production cost from        *
     * Cheaèness (nu_kappa)                                                   */
    double numOfComp;
    /* Number of components required for each computer                        */
    double phi;
    /* Scale parameter in Equation 1 (PHI_kappa)                              */
    int rangeLengthContr;
    /* Range of duration of a contract with a component supplier (T-CO_f,t)   */
    double rdOnProf;
    /* Fraction of profit invested in R&D (phi-RD)                            */
    double rho;
    /* Elasticity-related parameter in Equation 1 (rho_kappa)                 */
    double tau;
    /* Weight of component in Equation 1 (tau_kapp                            */
    double theta;
    /* Angle defining technological trajectory (theta_kappa)                  */
    double[] sdCmp;
    /* Standard deviation of technical knowledge distribution for components  *
     * (sigma-RD_k)                                                           */
    double sdSys;
    /* Standard deviation of technical knowledge distribution for systems     *
     * (sigma-RD_kappa)                                                       */
    double weightExit;
    /* Weight of current market share for exit decision (w-E)                 */
    double xiInt;
    /* Integration parameter in Equation 17 (xi-I)                            */
    double xiSpec;
    /* Specialization parameter in Equation 17 (xi-S)                         */
    
    // VARIABLES
    double pkSys;
    /* System technology public knowledge (K-SY_kappa)                        */
    double[] pkCmp;
    /* Component technology public knowledge (K-CO_k)                         */
    
    // TECHNICAL VARIABLES & OBJECTS
    String id;
    /* Computer market identifier: "MAINFRAMES" or "PC"                       */
    int numOfFirms;
    /* Maximum number of firms that could be on the market                    */
    int tIdCmp;
    /* Identifier of the current prevailing component technology              */
    ComputerFirm[] Firm;
    /* Array of computer firms                                                */
    Random rng; 
    /* Random Number Generator                                                */
    
    // STATS VARIABLES
    double aliveFirms;
    /* Number of firms active in the market                                   */
    double herfindahlIndex;
    /* Herfindahl index                                                       */
    double intFirms;
    /* Number of integrated firms active in the market                        */
    double intRatio;
    /* Integration ratio                                                      */
    
    // CONSTRUCTOR
    ComputerMarket(String ID, int NUMOFFIRM, int BUYERS, double DELTAMOD,
      double DELTASHARE, double NUCOMPUTER, double NUCMP, boolean PC,
      double RDONPROF, double MARKUP, double STARTSHARE, double SPILLOVER,
      double NUMOFCOMP, double RHO, double TAU, double PHI, double MODSYS,
      double INTERNALCUM, int MINLENGTHCONTR, int RANGELENGTHCONTR,
      double XIINT, double CHI1, double CHI2, double CHI0, double XISPEC,
      int MININTTIME, double INHERITANCE, int[] ENTRYTIMECMP,
      double[] LIMITSYSMOD, int ENTRYDELAYSYS, int ENTRYDELAYCMP, double THETA,
      double GAMMA, double SDSYS, double[] SDCMP, double[] L0CMP,
      double[] L1CMP, double[] L2CMP, double L0SYS,double L1SYS, double L2SYS,
      double DRAWCOSTSYS, double[] DRAWCOSTCMP,int ENTRYTIMESYSTEC,
      double WEIGHTEXIT, double EXITHRESHOLD, Random RNG) {
        
        id               = ID;
        numOfFirms       = NUMOFFIRM;
        buyers           = BUYERS;
        deltaMod         = DELTAMOD;
        deltaShare       = DELTASHARE;
        nuComputer       = NUCOMPUTER;
        nuCmp            = NUCMP;
        numOfComp        = NUMOFCOMP;
        rho              = RHO;
        tau              = TAU;
        theta            = THETA;
        phi              = PHI;
        minLengthContr   = MINLENGTHCONTR;
        rangeLengthContr = RANGELENGTHCONTR;
        xiInt            = XIINT;
        chi1             = CHI1;
        chi2             = CHI2;
        chi0             = CHI0;
        xiSpec           = XISPEC;
        minIntTime       = MININTTIME;
        inheritance      = INHERITANCE;
        entryTimeCmpTec  = ENTRYTIMECMP;
        limitSysMod      = LIMITSYSMOD;
        entryDelaySys    = ENTRYDELAYSYS;
        entryDelayCmp    = ENTRYDELAYCMP;
        gamma            = GAMMA;
        sdCmp            = SDCMP;
        sdSys            = SDSYS;
        l0Cmp            = L0CMP;
        l1Cmp            = L1CMP;
        l2Cmp            = L2CMP;
        l0Sys            = L0SYS;
        l1Sys            = L1SYS;
        l2Sys            = L2SYS;
        drawCostSys      = DRAWCOSTSYS;
        drawCostCmp      = DRAWCOSTCMP;
        entryTimeSysTec  = ENTRYTIMESYSTEC;
        markup           = MARKUP;
        rdOnProf         = RDONPROF;
        internalCum      = INTERNALCUM;
        weightExit       = WEIGHTEXIT;
        exitThreshold    = EXITHRESHOLD;
        rng              = RNG;
        
        pkCmp            = new double[3];
        pkSys            = 0;
        aliveFirms       = 0;
        herfindahlIndex  = 0;
        intFirms         = 0;
        intRatio         = 0;        
        tIdCmp           = 0;
        
        Firm = new ComputerFirm[1000];
        
        for (int i = 1; i <= numOfFirms; i++) {
            Firm[i] = new ComputerFirm(i, PC, STARTSHARE, SPILLOVER, MODSYS, this);
        }
    }

    /* This method switches reference to the latest component technology      */
    void changeCmpTechnology(int TIDCMP) {
        tIdCmp = TIDCMP;
    }

    /* This method controls the integration, specialization and supplier      *
     * selection decisions of computer firms                                  */
    void contractEngine(ComponentMarket CMP, int T, int START) {
        
        double bestCmpMod = CMP.modOfBestProducer();
        double qCO        = CMP.sizeOfBiggestProducer();
                
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                double randomNumber = rng.nextDouble();
                
                /* CASE 1: The firm just entered the market                   */
                if (Firm[f].born) {
                    Firm[f].born = false;
                    int newSupplier = CMP.chooseFirm();
                    if (newSupplier != -1) {
                        Firm[f].signContract(newSupplier, T, CMP.Firm[newSupplier].tId);
                        CMP.Firm[newSupplier].signContract(START + f);
                    } else {
                        Firm[f].exitFirm();
                    }
                }
                
                /* CASE 2: The firm is specialized and its contract just      * 
                 * expired                                                    */ 
                if ((!Firm[f].integrated) && ((T - Firm[f].contractTime) >= Firm[f].contractD)) {
                    Firm[f].calcProbToIntegrate(qCO, T);
                    if (Firm[f].probToInt >= randomNumber) {
                        CMP.Firm[Firm[f].supplierId].cancelContract(START + f);
                        Firm[f].integrateVertically(CMP.Firm[Firm[f].supplierId],T);
                    } else {
                        int newSupplier = CMP.chooseFirm();
                        if (newSupplier != -1) {
                            CMP.Firm[Firm[f].supplierId].cancelContract(START + f);
                            Firm[f].signContract(newSupplier, T, CMP.Firm[newSupplier].tId);
                            CMP.Firm[newSupplier].signContract(START + f);
                        }
                    }
                }
                
                /* CASE 3: The firm is integrated and the minimum integration *
                 * period is expired                                          */
                if ((Firm[f].integrated) && (T - Firm[f].intTime > minIntTime)) {
                    if (bestCmpMod > 0) {
                        Firm[f].calcProbToSpecialize(bestCmpMod);
                        if (Firm[f].probToSpec >= randomNumber) { //aggiunto =
                            int newSupplier = CMP.chooseFirm();
                            if (newSupplier != -1) {
                                Firm[f].signContract(newSupplier, T, CMP.Firm[newSupplier].tId);
                                CMP.Firm[newSupplier].signContract(START + f);
                            }
                        }
                    }
                }
            }
        }
    }

    /* This method calls the firm-level method regulating R&D expenditure     */
    void rdExpenditure() {
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].rdExpenditure();
            }
        }
    }
    
    /* This method updates the level of public knowledge of all existing      *
     * component technologies and then if the firm is integrated it calls for *
     * the firm-level method controlling component technical progress,        *
     * otherwise it updates the component mod of the supplier                 */
    void modComponentProgress(int TT, ComponentMarket CMP) {
        
        pkCmp[0]  = l0Cmp[0] * Math.exp(l1Cmp[0] * TT) * (1 - 1 / (l2Cmp[0] * (TT - (entryTimeCmpTec[0] - entryDelayCmp))));
        
        if (TT > (entryTimeCmpTec[1] - entryDelayCmp)) {
            pkCmp[1] = l0Cmp[1] * Math.exp(l1Cmp[1] * TT) * (1 - 1 / (l2Cmp[1] * (TT - (entryTimeCmpTec[1] - entryDelayCmp))));
        }

        if (TT > (entryTimeCmpTec[2] - entryDelayCmp)) {
            pkCmp[2] = l0Cmp[2] * Math.exp(l1Cmp[2] * TT) * (1 - 1 / (l2Cmp[2] * (TT - (entryTimeCmpTec[2] - entryDelayCmp))));
        }

        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) { 
                if (Firm[f].integrated) {
                    Firm[f].checkComponentTechnology(TT, pkCmp);
                    Firm[f].progressCmp();
                }
                else {
                    Firm[f].Component.mod = CMP.Firm[Firm[f].supplierId].Component.mod;
                    Firm[f].Component.productionCost = CMP.Firm[Firm[f].supplierId].Component.productionCost;
                    Firm[f].tId                      = CMP.Firm[Firm[f].supplierId].tId;
                }
            }
        }
        
    }
    
    /* This method updates the level of public knowledge of the relevant      *
     * system technology and then it calls for the firm-level method          *
     * controlling system technical progress                                  */
    void modSystemProgress(int TIME) {
        
        if (TIME >= 1) {
            pkSys = l0Sys * Math.exp(l1Sys * TIME) * (1 - (1 / (l2Sys * (TIME - (entryTimeSysTec - entryDelaySys)))));
        }

        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].progressSys();
            }
        }
    }
    
    /* This method calls the firm-level method controlling the mod, cost and  *
     * price of the computer product after progress in components and systems *
     * has occurred                                                           */
    void computerModCostPrice() {
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].computerModPriceCost();
            }
        }
    }
    
    /* This method computes the propensities and probabilities to sell        *
     * computers to customers by calling the corresponding firm-level methods *
     * and then it computes the quantity sold                                 */
    void probOfSelling() {
        
        double sumPtS = 0;
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].Computer.calcPropToSell();
                sumPtS += Firm[f].Computer.u;
            }
        }
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].Computer.calcProbToSell(sumPtS);
            }
        }
        int demand[] = new int[buyers];
        for (int g = 0; g < buyers; g++) {
            demand[g]           = 0;
            double cumulated    = 0;
            double randomNumber = rng.nextDouble();
            boolean assigned    = false;
            int f               = 1;
            while ((!assigned) && (f <= numOfFirms)) {
                if (Firm[f].alive) {
                    cumulated += Firm[f].Computer.U;
                    if (randomNumber < cumulated) {
                        demand[g] = Firm[f].id;
                        assigned    = true;
                    }
                }
                f++;
            }
        }
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                int count = 0;
                for (int g = 0; g < buyers; g++) {
                    if (demand[g] == Firm[f].id) {
                        count++;
                    }
                }
                Firm[f].calcQuantitySold(count);
            }
        }
    }
    
    /* This method calls for firm-level methods computing profit and market   *
     * share                                                                  */
    void accounting(int t) {
        
        double totSold = 0;
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].accounting();
                totSold += Firm[f].qSold;
            }
        }
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].calcShare(totSold);
            }
        }
    }
    
    /* This method calls firm-level methods controlling the exit conditions,  *
     * and in the case of a failed specialized firm it also updates the       *
     * buyers list of the corresponding supplier                              */
    void checkExit(ComponentMarket CMP, int START) {
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                boolean exit = Firm[f].exitTheMarket();
                if (exit) {
                    if (!Firm[f].integrated) {
                        if (CMP.Firm[Firm[f].supplierId].buyerId[START + f] == 1) {
                            CMP.Firm[Firm[f].supplierId].cancelContract(START + f);
                        }
                    }
                    Firm[f].exitFirm();
                }
            }
        }
    }
    
    /* This method computes the relevant statistics about the computer        *
     * market                                                                 */
    void statistics(int time) {
        
        aliveFirms       = 0;
        herfindahlIndex  = 0;
        intFirms         = 0;
        intRatio         = 0;        

        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                aliveFirms++;

                if (Firm[f].integrated) {
                    intFirms++;
                }
            }
        }
        if (aliveFirms == 0) {
            intRatio        = 0;
            herfindahlIndex = 1;
        }
        else {
            intRatio = intFirms / aliveFirms;
            for (int f = 1; f <= numOfFirms; f++) {
                if (Firm[f].alive) {
                    herfindahlIndex  += Math.pow(Firm[f].share, 2);
                }
            }
        }          
    }
    
}
