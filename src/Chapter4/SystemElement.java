package Chapter4;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables that define the system element produced  *
 * by computer firms and the methods that operate over these variables        */
class SystemElement {
    
    // VARIABLES
    double mod;
    /* Merit of design of the system element (M-SY_f,t)                       */
    double muProg;
    /* Mean of the distribution of system technical progress (mu-SY_f,t)      */
    
    //TECHNICAL VARIABLES & OBJECTS
    ComputerFirm Firm;
    /* Access to the firm                                                     */
    
    // CONSTRUCTOR
    SystemElement(double MOD, ComputerFirm FIRM) {
        mod  = MOD;
        Firm = FIRM;
    }

    /* This method computes the mod of the system based on the level of past  *
     * mod and the level of public knowledge                                  */
    void calcMod() {
        
        double zmax = 0;
        /* Equation 14.a                                                      */
        muProg = Math.log(Firm.ComputerMarket.pkSys) * (1 - Firm.ComputerMarket.internalCum)
                 + Math.log(mod) * Firm.ComputerMarket.internalCum;
        for (int i = 1; i <= Firm.numOfDrawsSys; i++) {
            double z = Math.exp(muProg + Math.sqrt(Firm.ComputerMarket.sdSys)
                         * Firm.ComputerMarket.rng.nextGaussian());
            if (z > zmax) {
                zmax = z;
            }
        }
        if (zmax > mod) {
            mod = zmax;
        }
    }
    
    /* This method is activated when exit occurs: it resets the most relevant *
     * variables at the product level                                         */
    void exitSystem() {
        muProg  = 0;
        mod     = 0;
    }
}
