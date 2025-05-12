package Chapter4;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables that define the computer product and the *
 * methods that operate over these variables                                  */
class EndProduct {
    
    // VARIABLES
    double cheap;
    /* Cheapness of the computer product (Z-CH_f,t)                           */
    double mod;
    /* Merit of design of the computer product (M_f,t)                        */
    double modForCust;
    /* Merit of design as perceived by customers of user class h (M_f,h,t)    */
    double perf;
    /* Performance of the computer product (Z-PE_f,t)                         */
    double productionCost;
    /* Computer production cost (C-CO_f,t)                                    */
    double u;
    /* Propensity of computer to be sold to customers (u_f,h,t)               */
    double U;
    /* Probability of computer to be sold to customers (U_f,h,t)              */

    //TECHNICAL VARIABLES & OBJECTS
    ComputerFirm Firm;
    /* Access to the firm                                                     */
    
    // CONSTRUCTOR
    EndProduct(ComputerFirm FIRM) {
        cheap          = 0;
        perf           = 0;
        mod            = 0;
        modForCust     = 0;
        productionCost = 0;
        u              = 0;
        U              = 0;
        Firm           = FIRM;
    }

    /* This method computes the mod of the computer based on the level of the *
     * mod of the component and the system element                            */
    void calcMod() {
        if (Firm.SysteM.mod > Firm.ComputerMarket.limitSysMod[Firm.tId]) {
            /* Equation 1. See also footnote 14 about technological limits    *
             * for the mod of the system element                              */
            mod = Firm.ComputerMarket.phi * Math.pow(
                    Firm.ComputerMarket.tau
                    * Math.pow(Firm.Component.mod, -Firm.ComputerMarket.rho)
                    + (1 - Firm.ComputerMarket.tau)
                    * Math.pow(Firm.ComputerMarket.limitSysMod[Firm.tId], -Firm.ComputerMarket.rho),
                      -(1 / Firm.ComputerMarket.rho));
        }
        else {
            /* Equation 1                                                     */
            mod = Firm.ComputerMarket.phi * Math.pow(
                    Firm.ComputerMarket.tau
                    * Math.pow(Firm.Component.mod, -Firm.ComputerMarket.rho)
                    + (1 - Firm.ComputerMarket.tau)
                    * Math.pow(Firm.SysteM.mod, -Firm.ComputerMarket.rho),
                      -(1 / Firm.ComputerMarket.rho));
        }
    }

    /* This method computes cheapness and performance of the computer, given  *
     * its mod                                                                */
    void calcCheapPerf() {
        cheap = mod * Math.cos(Firm.ComputerMarket.theta);
        perf  = mod * Math.sin(Firm.ComputerMarket.theta);
    }
    
    /* This method computes the production cost of the computer               */
    void calcCost() {
        /* Equation 9                                                         */
        productionCost = Firm.price / (1 + Firm.ComputerMarket.markup);
    }

    /* This method computes the mod as perceived by customers in the specific *
     * user class and the corresponding propensity to sell to these customers */
    void calcPropToSell() {
        /* Equation 3                                                         */
        modForCust = Math.pow(cheap, Firm.ComputerMarket.gamma)
                   * Math.pow(perf, 1 - Firm.ComputerMarket.gamma);
        /* Equation 2                                                         */
        u          = Math.pow(modForCust, Firm.ComputerMarket.deltaMod)
                   * Math.pow(1 + Firm.share, Firm.ComputerMarket.deltaShare);
    }
    
    /* This method computes the probability to sell                           */
    void calcProbToSell(double SUMPTS) {
        /* Equation 4                                                         */
        U = u/SUMPTS;
    }
    
    /* This method is activated when exit occurs: it resets the most relevant *
     * variables at the product level                                         */
    void exitComputer() {
        cheap          = 0;
        perf           = 0;
        mod            = 0;
        modForCust     = 0;
        productionCost = 0;
        u              = 0;
        U              = 0;
    }
    
}
