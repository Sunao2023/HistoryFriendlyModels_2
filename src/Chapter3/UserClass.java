package Chapter3;

import java.util.Random;

/*                                                                            *
 *  @author Gianluca Capone and Davide Sgobba                                 *
 *                                                                            */

/* This class contains all variables and parameters that refer to the demand  *
 * side and are common for all firms or defined at the aggregate level, and   *
 * the methods that operate over these variables or call for firm-level       *
 * methods                                                                    */
class UserClass {

    // PARAMETERS
    double brandLoyalty;
    /* Percentage of customers returning to the same computer (non activated) */
    double deltaA;
    /* Exponent of brand image (marketing capabilities) in Equation 9         *
     * (delta-A_h)                                                            */
    double deltaMod;
    /* Exponent of mod in Equation 9 (delta-M_h)                              */
    double deltaShare;
    /* Exponent of bandwagon (market share) in Equation 9 (delta-s_h)         */
    double gammaCheap;
    /* Exponent of cheapness in Equation 8 (gamma-CH_h)                       */
    double gammaMod;
    /* Scale parameter in Equation 8 (gamma-M_h)                              */
    double gammaPerf;
    /* Exponent of performance in Equation 8 (gamma-PE_h)                     */
    double lambdaA;
    /* Minimum level of marketing capabilities in Equation 9 (lambda-A)       */
    double lambdaCheap;
    /* Minimum cheapness level in Equation 8 (lambda-CH_h)                    */
    double lambdaF;
    /* Minimum threshold for full market activity (lambda-F_h)                */
    double lambdaPerf;
    /* Minimum performance level in Equation 8 (lambda-PE_h)                  */
    double lambdaShare;
    /* Minimum level of market share in Equation 9 (lambda-s_h)               */
    double minPropError;
    /* Minimum value of random factor in Equation 9 (e-u_f,t)                 */
    double numOfPotentialBuyers;
    /* Number of groups of potential customers (G_h)                          */    
    double rangePropError;
    /* Range of random factor in Equation 9 (e-u_f,t)                         */
    double theta;
    /* Probability of computer breakdown (THETA_h)                            */
    
    // VARIABLES
    double size;
    /* Size of the user class, that is number of computers sold to buyers     *
     * from the user class in the current period                              */
    
    // TECHNICAL VARIABLES & OBJECTS
    boolean fullMarket;
    /* This variable is initialized as "FALSE", and it takes value "TRUE"     *
     * once the number of active firms is equal to the threshold for full     *
     * market activity                                                        */
    Random rng;
    /* Random Number Generator                                                */
    
    // STATS VARIABLES
    double herfindahl;
    /* Herfindahl index                                                       */
    double meanCheap;
    /* Average cheapness level of active firms                                */
    double meanPerf;
    /* Average performance level of active firms                              */
    double numOfAdoptingFirms;
    /* Number of first generation firms using microprocessor technology       * 
     * (defined only in the Large Organizations User Class)                   */
    double numOfDiversifiedFirms;
    /* Number of diversified firms (defined only in the Small Users           *
     * & Individuals User Class)                                              */
    double numOfFirstGenFirms;
    /* Number of first generation active firms                                */
    double numOfSecondGenFirms;
    /* Number of second generation active firms                               */
    double share1stGen;
    /* Total market share of first generation firms                           */
    double share2ndGen;
    /* Total market share of second generation firms                          */
    double shareBest2nd;
    /* Market share of the best second generation firm                        */
    double shareDiv;
    /* Total market share of diversified firms                                *
     * (defined only in the Large Organizations User Class)                   */
    
    
    // CONSTRUCTOR
    /* Here parameters are initialized to values passed from outside the      *
     * class. Common parameters are equal across the twp user classes;        *
     * specific parameter values differ across classes.                       *
     * Variables are initialized at suitable values.                          */ 
    UserClass(String[] COMMONPAR, String[] SPECIFICPAR, Random RNG) {
        
        gammaMod             = Double.parseDouble(SPECIFICPAR[1]);
        gammaCheap           = Double.parseDouble(SPECIFICPAR[2]);
        lambdaCheap          = Double.parseDouble(SPECIFICPAR[3]);
        gammaPerf            = Double.parseDouble(SPECIFICPAR[4]);
        lambdaPerf           = Double.parseDouble(SPECIFICPAR[5]);
        deltaMod             = Double.parseDouble(SPECIFICPAR[6]);
        deltaShare           = Double.parseDouble(SPECIFICPAR[7]);
        deltaA               = Double.parseDouble(SPECIFICPAR[8]);
        lambdaF              = Double.parseDouble(SPECIFICPAR[9]);
        brandLoyalty         = Double.parseDouble(SPECIFICPAR[10]);
        lambdaShare          = Double.parseDouble(SPECIFICPAR[11]);
        theta                = Double.parseDouble(SPECIFICPAR[12]);
        
        minPropError         = Double.parseDouble(COMMONPAR[1]);
        rangePropError       = Double.parseDouble(COMMONPAR[2]);
        lambdaA              = Double.parseDouble(COMMONPAR[3]);
        numOfPotentialBuyers = Integer.parseInt(COMMONPAR[4]);
        
        rng          = RNG;
        fullMarket   = false;
        
        meanCheap    = 0;
        meanPerf     = 0;
        size         = 0;
        
        share1stGen  = 0;
        share2ndGen  = 0;
        shareBest2nd = 0;
        shareDiv     = 0;
        herfindahl   = 0;
        
        numOfFirstGenFirms    = 0;
        numOfAdoptingFirms    = 0;
        numOfSecondGenFirms   = 0;
        numOfDiversifiedFirms = 0;
    }
    
    /* This is an ancillary method and it is used to reset to zero            *
     * the variables before they take a new current value                     */    
    void resetStats() {
    
        meanCheap    = 0;
        meanPerf     = 0;
        size         = 0;
        
        share1stGen  = 0;
        share2ndGen  = 0;
        shareBest2nd = 0;
        shareDiv     = 0;
        herfindahl   = 0;
        
        numOfFirstGenFirms    = 0;
        numOfAdoptingFirms    = 0;
        numOfSecondGenFirms   = 0;
        numOfDiversifiedFirms = 0;
    }
    
    
    /* This is the main method of User Class, where market operations and     *
     * statistics are computed                                                */    
    void market(Industry industry, int t) {
            
        resetStats();
        
        /* Technical variables used only in this method are defined here      */
        double numOfPurchasingBuyers = 0;
        double cumulatedProb         = 0;
        double numOfSellingFirms     = 0;
        double busyBuyers            = 0;
        
        // This cycle checks the entry of firms
        for (int f = 1; f <= industry.numberOfFirms; f++) {
            if (industry.firms[f].alive) {
                industry.firms[f].checkEntry(t,this);
            }
        }
        
        /* This cycle computes the number of different firm categories active *
         * in the User Class and calls for the methods computing the mod as   *
         * perceived by buyers of the user class                              */
        for (int f = 1; f <= industry.numberOfFirms; f++) {
            if ((industry.firms[f].alive) && (industry.firms[f].servedUserClass == this)) {
                numOfSellingFirms++;

                if (industry.firms[f].generation == 1) {
                    numOfFirstGenFirms++;

                    /* This is properly defined only in the LO User Class     */
                    if (industry.firms[f].adopted) {
                        numOfAdoptingFirms++;
                    }
                }

                if (industry.firms[f].generation == 2) {
                    numOfSecondGenFirms++;
                }

                /* This is properly defined only in the SUI User Class        */
                if (industry.firms[f].generation == 3) {
                    numOfDiversifiedFirms++;
                }

                /* The local variable propError represents the random factor  *
                 * in Equation 9 (e-u_f,t)                                    */
                double propError = minPropError + rng.nextDouble() * rangePropError;
                industry.firms[f].calcMod(propError);
                
                cumulatedProb += industry.firms[f].u;
                
                busyBuyers += industry.firms[f].numberOfServedBuyers
                            + industry.firms[f].numberOfBLReturns;
            }
        }
        
        /* The number of actual buyers in the current period is determined    */
        if (!fullMarket && numOfSellingFirms <= lambdaF) {
            numOfPurchasingBuyers = (int) ((numOfPotentialBuyers - busyBuyers)
                                  * (double) numOfSellingFirms / lambdaF);
        } else {
            fullMarket = true;
            numOfPurchasingBuyers = numOfPotentialBuyers - busyBuyers;
        }
        
        /* This cycle computes market share variables and other statistics    *
         * first at the firm level and then at the aggregate level            */
        for (int f = 1; f <= industry.numberOfFirms; f++) {
            if ((industry.firms[f].alive) && (industry.firms[f].servedUserClass == this)) {
                
                industry.firms[f].calcSharePriceProfit(cumulatedProb, numOfPurchasingBuyers);
                
                herfindahl += industry.firms[f].share * industry.firms[f].share;
                size       += industry.firms[f].qSold;
                meanCheap  += industry.firms[f].computer.cheap;
                meanPerf   += industry.firms[f].computer.perf;
           
                if (industry.firms[f].generation == 1) {
                    share1stGen += industry.firms[f].share;
                }
                if (industry.firms[f].generation == 2) {
                    share2ndGen += industry.firms[f].share;
                    if (industry.firms[f].share >= shareBest2nd)  {
                        shareBest2nd = industry.firms[f].share;
                    }
                }
                if (industry.firms[f].generation == 3) {
                    shareDiv += industry.firms[f].share;
                }
            }
        }

        if (numOfSellingFirms > 0) {
            meanCheap /= numOfSellingFirms;
            meanPerf /= numOfSellingFirms;
        }
    }
    
}