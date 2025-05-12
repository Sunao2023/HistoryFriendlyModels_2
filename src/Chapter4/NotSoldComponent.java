package Chapter4;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables that define the component product        *
 * produced by integrated computer firms and the methods that operate over    *
 * these variables                                                            */
class NotSoldComponent {
    
    // VARIABLES
    double mod;
    /* Merit of design of the component product (M-CO_f,t)                    */
    double muProg;
    /* Mean of the distribution of component technical progress (mu-CO_f,t)   */
    double productionCost;
    /* Component production cost (C-CO_f,t)                                   */

    //TECHNICAL VARIABLES & OBJECTS
    ComputerFirm Firm;
    /* Access to the firm                                                     */
    
    // CONSTRUCTOR
    NotSoldComponent(ComputerFirm FIRM) {
        mod            = 0;
        muProg         = 0;
        productionCost = 0;
        Firm           = FIRM;
    }

    /* This method computes the mod of the component based on the level of    *
     * past mod and the level of public knowledge                             */
    void calcMod() {
        
        double zmax = 0;
        /* Equation 14.b                                                      */
        muProg = Math.log(Firm.ComputerMarket.pkCmp[Firm.tId]) * (1 - Firm.ComputerMarket.internalCum)
                      + Math.log(mod) * Firm.ComputerMarket.internalCum;
        for (int i = 1; i <= Firm.numOfDrawsCmp; i++) {
            double z = Math.exp(muProg + Math.sqrt(Firm.ComputerMarket.sdCmp[Firm.tId])
                         * Firm.ComputerMarket.rng.nextGaussian());
            if (z > zmax) {
                zmax = z;
            }
        }
        if (zmax > mod) {
            mod = zmax;
        }
        if (mod > 0) {
            /* Equation 11                                                    */
            productionCost = Firm.ComputerMarket.nuCmp / mod;
        }
    }
    
    /* This method is activated when exit occurs: it resets the most relevant *
     * variables at the product level                                         */
    void exitComponent() {
        muProg  = 0;
        mod            = 0;
        productionCost = 0;
    }
    
}
