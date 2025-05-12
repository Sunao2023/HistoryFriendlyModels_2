package Chapter3;

import java.util.Random;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables and parameters that refer to the supply  *
 * side and are common for all firms or defined at the aggregate level, and   *
 * the methods that operate over these variables or call for firm-level       *
 * methods                                                                    */
class Industry {
    
    // PARAMETERS
    double adv0;
    /* Scale parameter for marketing capabilities (a-0)                       */
    double adv1;
    /* Exponent for marketing capabilities (a-1)                              */
    double alphaAdo;
    /* Difficulty in the perception of the new technology to be adopted       *
     * (alpha-AD)                                                             */
    double alphaTr;
    /* Weight of distance from the Transistors technological frontier         *
       in determining adoption probability (alpha-TR)                         */
    double alphaMp;
    /* Weight of the advancement of the Microprocessor Technology             *
     * in determining adoption probability (alpha-MP)                         */
    double betaRes;
    /* Weight of R&D investment for technological change  (beta-R)            */
    double betaExp;
    /* Weight of technological experience for technological change (beta-EX   */
    double betaLim;
    /* Weight of distance from technological frontier for                     *
     * technological change (beta-LAMBDA)                                     */
    double betaCheap;
    /* Scale parameter for technological change in the cheapness dimension    *
     * (beta-CH                                                               */
    double betaPerf;
    /* Scale parameter for technological change in the performance dimension  *
     * (beta-PE)                                                              */
    double exitThreshold;
    /* Minimum threshold for exit (lambda-E)                                  */
    double fixedAdo;
    /* Fixed cost of adoption of the new technology (C-AD)                    */
    double markUp;
    /* Markup (m)                                                             */
    double muInn;
    /* Mean of random disturbance of technological change (mu-e)              */ 
    double nu;
    /* Proportionality factor to compute price from cheapness (nu)            */
    double phiAdo;
    /* Fraction of accumulated resources allocated to the adoption            *
     * of the new technology (phi-AD)                                         */ 
    double phiAdv;
    /* Fraction of profits after debt repayment allocated to                  *
     * advertising expenditures (phi-A)                                       */
    double phiBDiv;
    /* Fraction of initial budget spent by a diversifying entrant             *
     * in each period (phi-B)                                                 */
    double phiDebt;
    /* Fraction of profits allocated to debt repayment (phi-DB)               */
    double phiDiv;
    /* Fraction of accumulated resources transferred to                       *
     * the diversifying division (phi-DV)                                     */
    double phiExpMin;
    /* Minimum fraction of experience transferred to the adopted technology   *
     * (phi-EX)                                                               */
    double phiExpBias;
    /* Range of the fraction of experience transferred to the                 *
     * adopted technology (phi-EX)                                            */
    double phiRdTildMin;
    /* Minimum fraction of past R&D expenditure that must be spent            *
     * in the current period (phitilde-RD)                                    */
    double phiRdTildBias;
    /* Range of fraction of past R&D expenditure that must be spent           *
     * in the current period (phitilde-RD)                                    */
    double projectTime;
    /* Periods to develop a computer project (T-D)                            */
    double projTimeDiv;
    /* Periods to develop a computer project - diversifying firm (T-DV)       */
    double psiDiv;
    /* Spillover of marketing capabilities to the                             *
     * diversifying division (psi-DV)                                         */
    double phiRd;
    /* Fraction of profits after debt repayment allocated                     *
     * to R&D expenditures (phi-RD)                                           */
    double r;
    /* Interest rate (r)                                                      */
    double rdCost;
    /* Unit cost of R&D (C-RD)                                                */
    double sigmaInn;
    /* Std deviation of random disturbance of technological change (sigma-e)  */
    double weightExit;
    /* Weight of current performance in exit decision (w-E)                   */
    
    // VARIABLES
    int numberOfFirms;
    /* Number of firms potentially active in the computer industry            */

    // TECHNICAL VARIABLES & OBJECTS
    Firm[] firms;
    /* Array of firms                                                         */
    Random rng;
    /* Random Number Generator                                                */
    
    // CONSTRUCTOR
    /* Here parameters are initialized to values passed from outside the      *
     * class. Variables are initialized at suitable values.                   */ 
    Industry(String[] PARAMETERS, Technology TEC, Random RNG) {
                                            
        projectTime       = Double.parseDouble(PARAMETERS[1]);
        rdCost            = Double.parseDouble(PARAMETERS[2]);
        phiAdv            = Double.parseDouble(PARAMETERS[3]);
        adv0              = Double.parseDouble(PARAMETERS[4]);
        adv1              = Double.parseDouble(PARAMETERS[5]);
        alphaTr           = Double.parseDouble(PARAMETERS[6]);
        alphaMp           = Double.parseDouble(PARAMETERS[7]);
        alphaAdo          = Double.parseDouble(PARAMETERS[8]);
        phiAdo            = Double.parseDouble(PARAMETERS[9]);
        fixedAdo          = Double.parseDouble(PARAMETERS[10]);
        phiExpMin         = Double.parseDouble(PARAMETERS[11]);
        phiExpBias        = Double.parseDouble(PARAMETERS[12]);
        phiDiv            = Double.parseDouble(PARAMETERS[13]);
        projTimeDiv       = Double.parseDouble(PARAMETERS[14]);
        phiBDiv           = Double.parseDouble(PARAMETERS[15]);
        markUp            = Double.parseDouble(PARAMETERS[16]);
        phiRd             = Double.parseDouble(PARAMETERS[17]);
        psiDiv            = Double.parseDouble(PARAMETERS[18]);
        betaLim           = Double.parseDouble(PARAMETERS[19]);
        betaRes           = Double.parseDouble(PARAMETERS[20]);
        betaExp           = Double.parseDouble(PARAMETERS[21]);
        betaPerf          = Double.parseDouble(PARAMETERS[22]);
        betaCheap         = Double.parseDouble(PARAMETERS[23]);
        sigmaInn          = Double.parseDouble(PARAMETERS[24]);
        muInn             = Double.parseDouble(PARAMETERS[25]);
        phiDebt           = Double.parseDouble(PARAMETERS[26]);
        r                 = Double.parseDouble(PARAMETERS[27]);
        phiRdTildMin      = Double.parseDouble(PARAMETERS[28]);
        phiRdTildBias     = Double.parseDouble(PARAMETERS[29]);
        weightExit        = Double.parseDouble(PARAMETERS[30]);
        exitThreshold     = Double.parseDouble(PARAMETERS[31]);
        nu                = Double.parseDouble(PARAMETERS[32]);
        
        rng               = RNG;
        firms             = new Firm[200];
        numberOfFirms     = TEC.numOfFirms;
        
        /* This cycle initializes first generation firms, passing them the    *
         * following information: ID, birth period (1), generation (1),       *
         * technlogy (TR), the random number generator,                       *
         * and access to the Supply object                                    */
        for (int f = 1; f <= numberOfFirms; f++) {
            firms[f] = new Firm(f, 1, 1, TEC, this, RNG);
        }
    }
    
    // METHODS
    
    /* This method creates a new cohort of firms using the new microprocessor *
     * technology (TEC = MP)                                                  */
    void secondGenerationCreation(int TIME, Technology TEC) {
        
        for (int f = numberOfFirms + 1; f <= TEC.numOfFirms + numberOfFirms; f++) {
            firms[f] = new Firm(f, TIME, 2, TEC, this, rng);
        }
        numberOfFirms += TEC.numOfFirms;
    }
  
    /* This method checks whether firm-level conditions for diversification   *
     * are met and creates a new diversified firm by calling a specific firm  *
     * constructor, through which the parent resources and capabilities can   *
     * be transferred. A firm-level method is called to update the budget     *
     * and the condition of the parent firm                                   */ 
    void diversification(int TIME, Technology TEC, UserClass SMALLUSERS, UserClass LARGEORGS) {

        for (int f = 1; f <= numberOfFirms; f++) {
            if ((firms[f].alive) && (!firms[f].mother) && (firms[f].servedUserClass == LARGEORGS)
             && (firms[f].tec == TEC) && (firms[f].normNw > 0) && (firms[f].bud > 0)) {
                
                numberOfFirms++;
                
                firms[numberOfFirms] = new Firm(numberOfFirms, TIME, TEC, firms[f].bud * phiDiv,
                                               firms[f].mktingCapab * psiDiv, this, SMALLUSERS, rng);

                firms[f].diversify();
            }
        }
    }
    
    /* This method calls the firm-level method regulating R&D investment      */
    void rdInvest(int TIME) {
        
        for (int f = 1; f <= numberOfFirms; f++) {
            if (firms[f].alive) {
                firms[f].rdInvestment(TIME);
            }
        }
    }
    
    /* This method calls the firm-level method regulating                     *
     * marketing investment                                                   */
    void mktingInvest(int TIME) {
        
        for (int f = 1; f <= numberOfFirms; f++) {
            if (firms[f].alive) {
                firms[f].advExpenditure(TIME);
            }
        }
    }
    
    /* This method gets information about the users of the MP technology and  *
     * calls the firm-level method checking whether occur the conditions for  *
     * the adoption of the new technology (NEWTEC = MP)                       */
    void adoption(Technology NEWTEC) {
        
        double bestMP = findBestMPDistance(NEWTEC);

        for (int f = 1; f <= numberOfFirms; f++) {
            if ((firms[f].alive) && (firms[f].entered) && (firms[f].tec != NEWTEC)) {
                firms[f].adoption(bestMP, NEWTEC);
            }
        }
    }
    
    /* This is an ancillary method for adoption: it computes the              *
     * technological level of the best microprocessor firm                    */
    double findBestMPDistance(Technology TEC) {
        
        double maxDistance = 0;

        for (int f = 1; f <= numberOfFirms; f++) {
            if ((firms[f].alive) && (firms[f].tec == TEC)) {
                double distance = firms[f].distanceCovered();
                if (distance > maxDistance) {
                    maxDistance = distance;
                }
            }
        }
        return maxDistance;
    }
    
    /* This method calls the firm-level method regulating                     *
     * technological progress activities                                      */
    void innovation() {
        
        for (int f = 1; f <= numberOfFirms; f++) {
            if (firms[f].alive) {
                firms[f].innovation();
            }
        }
    }

    /* This method calls the firm-level method regulating                     *
     * accounting activities                                      */
    void accounting(int TIME) {
        
        for (int f = 1; f <= numberOfFirms; f++) {
            if (firms[f].alive) {
                firms[f].accounting(TIME);
            }
        }
    }

}