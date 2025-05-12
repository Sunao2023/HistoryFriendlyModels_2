package Chapter4;

import java.util.Random;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all parameters and variables that refer to the         *
 * Component Market, and the methods that operate over these variables or     *
 * call for firm-level methods                                                */
class ComponentMarket {
 
    // PARAMETERS
    double deltaMod;
    /* Exponent of Mod in Equation 2 adapted to components (delta-M_h)        */
    double[] deltaShare;
    /* Exponent of Market Share in Equation 2 adapted to components           *
     * (delta-s_k)                                                            */
    double[] drawCost;
    /* Draw cost for component technology in Equation 13.b (C-RD_k)           */
    int entryDelayCmp;
    /* Delay between component technology emergence and entry time of         *
     * component firms (T-CO)                                                 */
    int[] entryTimeCmpTec;
    /* Entry time of component firms, by component technology (T_k)           */
    int exitThreshold;
    /* Maximum number of periods a component firm can stay without selling    *
     * to computer firms (T-E)                                                */
    int[] externalMkts;
    /* Number of external markets, by component technology (G-CO_k)           */
    double internalCum;
    /* Weight of internal mod in the development of new knowledge (w-K)       */
    double[] l0;
    /* Baseline trajectory of component technology public knowledge in
     * Equation 15.b (l-0_k)                                                  */
    double[] l1;
    /* Asymptotic growth rate of component technology public knowledge in     *
     * Equation 15.b (l-1_k)                                                  */
    double[] l2;
    /* Speed of approach to asymptotic growth rate of component technology    *
     * public knowledge in Equation 15.b (l-2_k)                              */
    double markup;
    /* Markup (m)                                                             */
    double nu;
    /* Proportionality factor to compute production cost from Mod (nu_k)      */
    double rdOnProf;
    /* Fraction of profit invested in R&D (phi-RD)                            */
    double[] startModCmp;
    /* Initial value of component technology mod (M-CO_k)                     */
    double[] sdCmp;
    /* Standard deviation of of technical knowledge distribution for          *
     * components (sigma-RD_k)                                                */
    
    // VARIABLES
    double[] pk;
    /* Component technology public knowledge (K-CO_k)                         */
                    
    // TECHNICAL VARIABLES & OBJECTS
    int buyers;
    /* Number of computer firms that are potential buyers of component        *
     * products                                                               */
    int numOfFirms;
    /* Maximum number of firms that could be on the market                    */
    ComponentFirm[] Firm;
    /* Array of component firms                                               */
    Random rng;
    /* Random Number Generator                                                */
    
    // STATS VARIABLES
    double aliveFirms;
    /* Number of firms active in the market                                   */
    double  herfindahlIndex;
    /* Herfindahl index                                                       */
                    
    // CONSTRUCTOR
    ComponentMarket(int NUMOFFIRMS, double DELTAMOD, double DELTASHARE[],
      double NU, double RDONPROF, double MARKUP, double INTERNALCUM,
      double[] SDCMP, double[] DRAWCOSTCMP, double[] STARTMODCMP, double[] L0,
      double[] L1, double[] L2, int[] EXTERNALMKTS, int BUYERS,
      int EXITTHRESHOLD, int[] ENTRYTIMECMPTECH, int ENTRYDELAYCMP, Random RNG){
        
        numOfFirms       = NUMOFFIRMS;
        deltaMod         = DELTAMOD;
        deltaShare       = DELTASHARE;
        nu               = NU;
        sdCmp            = SDCMP;
        drawCost         = DRAWCOSTCMP;
        startModCmp      = STARTMODCMP;
        l0               = L0;
        l1               = L1;
        l2               = L2;
        externalMkts     = EXTERNALMKTS;
        buyers           = BUYERS;
        exitThreshold    = EXITTHRESHOLD;
        entryTimeCmpTec  = ENTRYTIMECMPTECH;
        entryDelayCmp    = ENTRYDELAYCMP;
        markup           = MARKUP;
        rdOnProf         = RDONPROF;
        internalCum      = INTERNALCUM;
        rng              = RNG;

        pk               = new double[3];
        
        Firm             = new ComponentFirm[100];
        
        for (int i = 1; i <= numOfFirms; i++) {
            Firm[i] = new ComponentFirm(i, 0, startModCmp[0], BUYERS, this);
        }
    }
    
    /* This method generates a new cohort of firms when a new component       *
     * technology emerges                                                                */
    void newEntry(int NF, int TID) {
        
        for (int i = (numOfFirms + 1); i <= (numOfFirms + NF); i++) {
            Firm[i] = new ComponentFirm(i, TID, startModCmp[TID], buyers, this);
        }
        numOfFirms += NF;
    }
    
    /* This method computes the propensities and probabilities to sell to     *
     * computer firms (before R&D activities of the period are performed) by  *
     * calling the corresponding firm-level methods                           */
    void rating() {
    
        double sumRating = 0;
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].Component.calcPropToSell();
                sumRating += Firm[f].Component.u;
            }
        }
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].Component.calcProbToSell(sumRating);
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
     * component technologies and then calls for the firm-level method        *
     * controlling technical progress                                         */
    void modProgress(int TIME) {
        
        /* Equation 15.b - Transistor technology                              */
        pk[0] =  l0[0] * Math.exp(l1[0] * TIME) * (1 - 1 / (l2[0] 
                          * (TIME - (entryTimeCmpTec[0] - entryDelayCmp))));
        
        if (TIME > entryTimeCmpTec[1] - entryDelayCmp) {
            /* Equation 15.b - Integrated Circuit technology                  */
            pk[1] = l0[1] * Math.exp(l1[1] * TIME) * (1 - 1 / (l2[1]
                             * (TIME - (entryTimeCmpTec[1] - entryDelayCmp))));
        }

        if (TIME > entryTimeCmpTec[2] - entryDelayCmp) {
            /* Equation 15.b - Microprocessor technology                      */
            pk[2] = l0[2] * Math.exp(l1[2] * TIME) * (1 - 1 / (l2[2] 
                             * (TIME - (entryTimeCmpTec[2] - entryDelayCmp))));
        }

        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].progress();
            }
        }
    }
    
    /* This method computes the propensities and probabilities to sell to     *
     * external markets (after R&D activities of the period are performed) by *
     * calling the corresponding firm-level methods and then it computes the  *
     * quantity sold to these markets                                         */
    void externalMkt() {
                
        for (int k = 0; k < 3; k++) {
            double sumPtS = 0;
            for (int f = 1; f <= numOfFirms; f++) {
                if (Firm[f].alive) {
                    if (Firm[f].tId == k) {
                        Firm[f].Component.calcPropToSellExt();
                        sumPtS += Firm[f].Component.uExt;
                    }
                }
            }
            for (int f = 1; f <= numOfFirms; f++) {
                if (Firm[f].alive) {
                    if (Firm[f].tId == k) {
                        Firm[f].Component.calcProbToSellExt(sumPtS);
                    }
                }
            }
            int externalMarket[] = new int[externalMkts[k]];
            for (int g = 0; g < externalMkts[k]; g++) {
                externalMarket[g]   = 0;
                double cumulated    = 0;
                double randomNumber = rng.nextDouble();
                boolean assigned    = false;
                int f               = 1;
                while ((!assigned) && (f <= numOfFirms)) {
                    if ((Firm[f].alive) && (Firm[f].tId == k)) {
                        cumulated += Firm[f].Component.UExt;
                        if (randomNumber < cumulated) {
                            externalMarket[g] = Firm[f].id;
                            assigned            = true;
                        }
                    }
                    f++;
                }
            }
            for (int f = 1; f <= numOfFirms; f++) {
                if ((Firm[f].alive) && (Firm[f].tId == k)) {
                    
                    int count = 0;
                    for (int g = 0; g < externalMkts[k]; g++) {
                        if (externalMarket[g] == Firm[f].id) {
                            count++;
                        }
                    }
                    Firm[f].calcExternalSold(count);
                }
            }
        }
    }
    
    /* This method calls for firm-level methods computing quantity, profit    *
     * and market share                                                       */
    void accounting(ComputerMarket MF, ComputerMarket PC, boolean PCENTRY) {
        
        double totSold = 0;
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].accounting(MF,PC,PCENTRY);
                totSold += Firm[f].totalSold;
            }
        }
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].calcShare(totSold);
            }
        }
    }

    /* This method calls firm-level methods controlling the exit conditions   */
    void checkExit() {
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                Firm[f].checkExit();
            }
        }
    }
    
    /* This method computes the relevant statistics about the component       *
     * market                                                                 */
    void statistics() {
        
        aliveFirms      = 0;
        herfindahlIndex = 0;

        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                aliveFirms++;
           }
        }
        
        if (aliveFirms == 0) {
            herfindahlIndex = 1;
        }
        else {
            for (int f = 1; f <= numOfFirms; f++) {
                if (Firm[f].alive) {
                    herfindahlIndex  += Math.pow(Firm[f].share, 2);
                }
            }
        }   
    }
    
    /* This is an ancillary method used by the Computer Market to select a    *
     * component firm to be used as a supplier on the basis of the rating     */
    int chooseFirm() {
        
        int     idRating     = 0;
        double  cumulated    = 0;
        double  randomNumber = rng.nextDouble();
        boolean chosen       = false;
        int     f            = 1;
        
        while ((!chosen) && (f <= numOfFirms)) {
            if (Firm[f].alive) {
                cumulated += Firm[f].Component.U;
                if (randomNumber < cumulated) {
                    idRating = f;
                    chosen   = true;
                }
            }
            f++;
        }
        return idRating;
    }

    /* This is an ancillary method to compute the size of the biggest         *
     * independent component producer                                         */
    double sizeOfBiggestProducer() {
        
        double maxSold = 0;
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                if (Firm[f].totalSold  >= maxSold) {
                    maxSold = Firm[f].totalSold;
                }
            }
        }
        return maxSold;
    }

    /* This is an ancillary method to compute the mod of the best independent *
     * component producer                                                     */
    double modOfBestProducer() {
        
        double maxMod = 0;
        for (int f = 1; f <= numOfFirms; f++) {
            if (Firm[f].alive) {
                if (Firm[f].Component.mod >= maxMod) {
                    maxMod = Firm[f].Component.mod;
                }
            }
        }
        return maxMod;
    }
    
}
