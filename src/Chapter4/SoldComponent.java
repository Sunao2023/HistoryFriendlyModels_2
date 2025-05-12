package Chapter4;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables that define the component product        *
 * produced by specialized component firms and the methods that operate over  *
 * these variables                                                            */
class SoldComponent {
    
    // VARIABLES
    double mod;
    /* Merit of design of the component product (M-CO_f,t)                    */
    double muProg;
    /* Mean of the distribution of component technical progress (mu-CO_f,t)   */
    double productionCost;
    /* Component production cost (C-CO_f,t)                                   */
    double u;
    /* Propensity of component to be sold to computer firms (u_f,h,t)         */
    double U;
    /* Probability of component to be sold to computer firms (U_f,h,t)        */
    double uExt;
    /* Propensity of component to be sold to external users (u_f,h,t)         *
     * See footnone 11 for the differences between u/U and uExt/UExt          */
    double UExt;
    /* Probability of component to be sold to external users (U_f,h,t)        */
    
    //TECHNICAL VARIABLES & OBJECTS
    ComponentFirm Firm;
    /* Access to the firm                                                     */
    
    // CONSTRUCTOR
    SoldComponent(double MOD, ComponentFirm FIRM) {
        muProg         = 0;
        productionCost = 0;
        u              = 0;
        U              = 0;
        uExt           = 0;
        UExt           = 0;
        mod            = MOD;
        Firm           = FIRM;
    }

    /* This method computes the propensity to sell to computer firms          */
    void calcPropToSell() {
        /* Equation 2 adapted to components                                   */
        u = Math.pow(mod, Firm.CmpMarket.deltaMod) 
             * Math.pow(1 + Firm.share, Firm.CmpMarket.deltaShare[Firm.tId]);
    }
    
    /* This method computes the probability to sell to computer firms         */
    void calcProbToSell(double SUMRAT) {
        /* Equation 4 adapted to components                                   */
        U = u/SUMRAT;
    }
    
    /* This method computes the mod of the component based on the level of    *
     * past mod and the level of public knowledge                             */
    void calcMod() {
        
        double zmax = 0;
        /* Equation 14.b                                                      */
        muProg = Math.log(Firm.CmpMarket.pk[Firm.tId]) * (1 - Firm.CmpMarket.internalCum)
                             + Math.log(mod) * Firm.CmpMarket.internalCum;
        for (int i = 1; i <= Firm.numOfDrawsCmp; i++) {
            double z = Math.exp(muProg + Math.sqrt(Firm.CmpMarket.sdCmp[Firm.tId])
                       * Firm.CmpMarket.rng.nextGaussian());
            if (z > zmax) {
                zmax = z;
            }
        }
        if (zmax > mod) {
            mod = zmax;
        }
        if (mod > 0) {
            /* Equation 11                                                    */
            productionCost = Firm.CmpMarket.nu / mod;
        }
    }
    
    /* This method computes the propensity to sell to external markets        */
    void calcPropToSellExt() {
        /* Equation 2 adapted to components                                   */
        uExt = Math.pow(mod, Firm.CmpMarket.deltaMod) 
             * Math.pow(1 + Firm.share, Firm.CmpMarket.deltaShare[Firm.tId]);
    }
    
    /* This method computes the probability to sell to external markets       */
    void calcProbToSellExt(double SUMPTS) {
        /* Equation 4 adapted to components                                   */
        UExt = uExt/SUMPTS;
    }
    
    /* This method is activated when exit occurs: it resets the most relevant *
     * variables at the product level                                         */
    void exitComponent() {
        muProg         = 0;
        productionCost = 0;
        u              = 0;
        U              = 0;
        uExt           = 0;
        UExt           = 0;
        mod            = 0;
    }
    
}