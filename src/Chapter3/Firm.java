package Chapter3;

import java.util.Random;
import jsc.distributions.Binomial;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables that define firm heterogeneity and the   *
 * methods that operate over these variables                                  */
class Firm {

    // VARIABLES
    double advExpend;
    /* Amount of resources invested in advertising (B-A_f,t)                  */
    double bud;
    /* Amount of available resources (B_f,t)                                  */
    int cheapRdInput;
    /* R&D investment in cheapness (R-CH_f,t)                                 */
    double debt;
    /* Amount of debt (DB_f,t)                                                */
    double exitVar;
    /* Variable controlling the exit decision of the firm (E_f,t)             */
    double experience;
    /* Experience of the firm in the current technology (EX_f,k,t)            */
    double initBud;
    /* Initial budget of firm (B-0_f)                                         */
    double mktingCapab;
    /* Marketing capabilities (A_f,t)                                         */
    double mod;
    /* Merit of a computer (M_f,h,t)                                          */
    double normNw;
    /* Normalized net worth                                                   */
    double numberOfBLReturns;
    /* Number of buyers that buy again from the same firm because of          *
     * brand loyalty                                                          */
    double numberOfBreakdowns;
    /* Number of buyers whose computers break down                            */
    double numberOfNewBuyers;
    /* Number of new buyers (G_f,h,t)                                         */
    double numberOfServedBuyers;
    /* Number of buyers that currently have a computer of the firm            */
    int perfRdInput;
    /* R&D investment in performance (R-PE_f,t)                               */
    double price;
    /* Price of the computer (P_f,t)                                          */
    double productionCost;
    /* Production cost of the computer (C-PD_f,t)                             */
    double profit;
    /* Profit (PI_f,t)                                                        */
    double qSold;
    /* Quantity of computers sold by the firm (q_f,h,t; q_f,t)                */
    double u;
    /* Propensity of computer to be sold (u_f,h,t)                            */
    double share;
    /* Probability of computer to be sold (U_f,h,t; s_f,t)                    */
    
    // TECHNICAL VARIABLES & OBJECTS
    boolean adopted;
    /* All firms start with "FALSE". It takes the value "TRUE" when a TR firm *
     * adopts the new MP technology                                           */
    boolean alive;
    /* All firms start with "TRUE"- It takes the value "FALSE" when the firm  *
     * fails                                                                  */
    Firm.Product computer;
    /* This object contains the information about the computer product        *
     * (Cheapness and Performance)                                            */
    Industry computerIndustry;
    /* This is an access to the common industry information                   */
    boolean entered;
    /* All firms start with "FALSE"- It takes the value "TRUE" when the firm  *
     * enters the MF or PC market                                             */
    int generation;
    /* Identifier of generation (1 = First Generation; 2 = Second Generation; *
     * 3 = Diversified                                                        */
    int id;
    /* Firm identifier                                                        */
    boolean mother;
    /* All firms start with "FALSE"- It takes the value "TRUE" when a TR firm *
     * enters the PC market through diversification                           */
    Random rng;
    /* Random Number Generator                                                */
    UserClass servedUserClass;
    /* This is an access to the user class served by the firm (LO, SUI)       */
    Technology tec;
    /* This object represents the technlogy to produce computers (TR, MP)     */
    int timeBirth;
    /* Time period of firm creation                                           */
    Firm.Trajectory traj;
    /* This object contains the information about the trajectory of the firm  *
     * in the technological space                                             */   
    
    
    // CONSTRUCTORS
    
    /* Constructor for regular firms. ServedUserClass is determined only when *
     * the firm enters. Characteristics differ across the two generations     */
    Firm(int ID, int TIMEBIRTH, int GENERATION, Technology TEC,
      Industry COMPUTERINDUSTRY, Random RNG) {
        
        alive                = true;
        adopted              = false;
        entered              = false;
        mother               = false;
        rng                  = RNG;
        id                   = ID;
        timeBirth            = TIMEBIRTH;

        generation           = GENERATION;
        tec                  = TEC;
        initBud              = TEC.minInitBud + rng.nextDouble() * TEC.rangeInitBud;
        bud                  = initBud;
        debt                 = initBud;
        mktingCapab          = 0;
        computerIndustry     = COMPUTERINDUSTRY;
        
        computer             = new Firm.Product();
        traj                 = new Firm.Trajectory();
        
        advExpend            = 0;
        exitVar              = 0;
        experience           = 0;
        mod                  = 0;
        normNw               = 0;
        share                = 0;
        numberOfBLReturns    = 0;
        numberOfBreakdowns   = 0;
        numberOfNewBuyers    = 0;
        numberOfServedBuyers = 0;
    }

    /* Constructor for diversified firms. Relevant information is inherited   *
     * from the parent firm                                                   */
    Firm(int ID, int TIMEBIRTH, Technology TEC, double INITBUD, double EBW,
      Industry COMPUTERINDUSTRY, UserClass USERCLASS, Random RNG) {
        
        alive                = true;
        adopted              = false;
        entered              = true;
        mother               = false;
        rng                  = RNG;
        id                   = ID;
        timeBirth            = TIMEBIRTH;

        generation           = 3;
        tec                  = TEC;
        initBud              = INITBUD;
        bud                  = INITBUD;
        debt                 = 0;
        mktingCapab          = EBW;
        computerIndustry     = COMPUTERINDUSTRY;
        servedUserClass      = USERCLASS;
        
        computer             = new Firm.Product();
        traj                 = new Firm.Trajectory();
        
        advExpend            = 0;
        exitVar              = 0;
        experience           = 0;
        mod                  = 0;
        normNw               = 0;
        share                = 0;
        numberOfBLReturns    = 0;
        numberOfBreakdowns   = 0;
        numberOfNewBuyers    = 0;
        numberOfServedBuyers = 0;
        
        computer.cheap       = USERCLASS.meanCheap;
        computer.perf        = USERCLASS.meanPerf;
    }
    
    
    // METHODS

    /* This method computes the R&D investment distinguishing four cases.     */
    void rdInvestment(int TIME) {
    
        int anteRd = cheapRdInput + perfRdInput;
        double curRDInvestProf = profit * (1 - computerIndustry.phiDebt) * computerIndustry.phiRd;
        
        /* Case 1: the firm is a first or second generation startup and it    *
         * still has resources from the initial project                       */
        if ((generation < 3) && (TIME - timeBirth < computerIndustry.projectTime)) {
            cheapRdInput = (int) Math.floor(((initBud / computerIndustry.projectTime + curRDInvestProf)
                                            * traj.cheapMix) / computerIndustry.rdCost);
            perfRdInput =  (int) Math.floor(((initBud / computerIndustry.projectTime + curRDInvestProf)
                                            * traj.perfMix) / computerIndustry.rdCost);
        }
        /* Case 2: the firm is diversified and it still has resources from    *
         * the initial project                                                */
        else if ((generation == 3) && (TIME - timeBirth < computerIndustry.projTimeDiv)) {
            cheapRdInput = (int) Math.floor((((initBud * computerIndustry.phiBDiv / computerIndustry.projTimeDiv)
                                    + curRDInvestProf) * traj.cheapMix) / computerIndustry.rdCost);
            perfRdInput =  (int) Math.floor((((initBud * computerIndustry.phiBDiv  / computerIndustry.projTimeDiv)
                                  + curRDInvestProf) * traj.perfMix) / computerIndustry.rdCost);
        }
        /* Case 3: firm's profit does not allow to keep the current level of  *
         * R&D expenditures                                                   */
        else if (curRDInvestProf < anteRd * computerIndustry.rdCost) {
            double decrease = computerIndustry.phiRdTildMin + rng.nextDouble() * computerIndustry.phiRdTildBias;
            cheapRdInput = (int) Math.floor(cheapRdInput * decrease);
            perfRdInput  = (int) Math.floor(perfRdInput * decrease);
        }
        /* Case 4: the firm invests in R&D according to the fraction of       *
         * profits rule                                                       */
        else {
            cheapRdInput = (int) Math.floor((curRDInvestProf * traj.cheapMix)
                                            / computerIndustry.rdCost);
            perfRdInput = (int) Math.floor((curRDInvestProf * traj.perfMix) 
                                            / computerIndustry.rdCost);
        }
        bud -= (cheapRdInput + perfRdInput) * computerIndustry.rdCost;
        int postRd = cheapRdInput + perfRdInput;
        if ((bud <= 0) || (postRd < 1)) {
            exitFirm();
        }
    }
    
    /* This method computes the advertising investment and its effects on     *
     * marketing capabilities                                                 */
    void advExpenditure(int TIME) {
        
        /* Equation 6                                                         */
        advExpend    = computerIndustry.phiAdv * profit * (1-computerIndustry.phiDebt);
        /* Equation 7                                                         */
        mktingCapab += computerIndustry.adv0 * Math.pow(advExpend, computerIndustry.adv1);
        bud -= advExpend;
        if (bud <= 0) {
            exitFirm();
        }
    }

    /* This method computes the mod of the computer as perceived by the       *
     * served user class, the propensity to buy of customers of this user     *
     * class, and the number of current customers that will be again on the   *
     * market because of product breakdown                                    */
    void calcMod(double PERCERROR) {
        
        if ((computer.cheap <= servedUserClass.lambdaCheap) || (computer.perf <= servedUserClass.lambdaPerf)) {
            mod = 0;
        }
        else {
            // Equation 8
            mod = (servedUserClass.gammaMod)
                * Math.pow((computer.cheap - servedUserClass.lambdaCheap), (servedUserClass.gammaCheap))
                * Math.pow((computer.perf - servedUserClass.lambdaPerf), (servedUserClass.gammaPerf));
        }
        
        // Equation 9
        u = Math.pow(mod, servedUserClass.deltaMod)
          * Math.pow(Math.max(servedUserClass.lambdaShare, share), servedUserClass.deltaShare)
          * Math.pow(Math.max(servedUserClass.lambdaA, mktingCapab), servedUserClass.deltaA)
          * PERCERROR;
        
        numberOfNewBuyers = 0;
        
        if (numberOfServedBuyers > 0) {
            Binomial nB = new Binomial((int) numberOfServedBuyers, servedUserClass.theta);
            nB.setSeed(rng.nextLong());
            numberOfBreakdowns = nB.random();
            numberOfBLReturns = (int) (numberOfBreakdowns * servedUserClass.brandLoyalty);
            numberOfServedBuyers -= numberOfBreakdowns;
            numberOfNewBuyers    = numberOfBLReturns;
        }
                
    }

    /* This method computes market share, price, production cost, profit      */
    void calcSharePriceProfit(double SUM, double BUYINGCUST) {
        if (SUM != 0) {
            /* Equation 10                                                    */
            share = u / SUM;
        }
        else {
            share = 0;
        }
        numberOfNewBuyers  += (int) Math.rint(share * BUYINGCUST);
        numberOfServedBuyers += numberOfNewBuyers;
        /* Equation 11                                                        */
        qSold = mod * numberOfNewBuyers;
        
        if (computer.cheap > 0) {
            /* Equation 2                                                     */
            price = (computerIndustry.nu / (computer.cheap));
        }
        else {
            price = 0;
        }
        // Equation 3
        productionCost = price / (1 + computerIndustry.markUp);
        // Equation 4
        profit = productionCost * computerIndustry.markUp * qSold;
        bud += profit;
    }

    /* This method updates the budget and the indicator of a firm that        *
     * diversifies into the SUI market with a new independent division        */
    void diversify() {
        bud = bud * (1 - computerIndustry.phiDiv);
        mother = true;
    }
    
    /* This method checks whether firm-level conditions for adoption of the   *
     * new technology are met and in case of adoption operates suitable       *
     * changes in the firm variables (budget, technology, adoption            *
     * controller, experience)                                                */ 
    void adoption(double bestMP, Technology NEWTEC) {

        /* Equation 12                                                        */
        double probability = Math.pow(0.5 * Math.pow(distanceFromCorner(), computerIndustry.alphaTr)
                                    + 0.5 * Math.pow(bestMP, computerIndustry.alphaMp), computerIndustry.alphaAdo);
        if (rng.nextDouble() < probability) {
            /* Equation 13                                                    */
            double budgetAfterAdoption = bud * (1 - computerIndustry.phiAdo) - computerIndustry.fixedAdo;
            if (budgetAfterAdoption > 0) {
                bud = budgetAfterAdoption;
                tec        = NEWTEC;
                adopted    = true;
                double e = (computerIndustry.phiExpMin + rng.nextDouble() * computerIndustry.phiExpBias) * experience;
                if (e < experience) {
                    experience = e;
                }
            }
        }
    }
    
    /* This is an ancillary method called by the adoptio method. It computes  *
     * the first element of the numerator in Equation 12                      */
    double distanceFromCorner() {
        return 1 - Math.sqrt((tec.cheapLim - computer.cheap) * (tec.cheapLim - computer.cheap)
                             + (tec.perfLim - computer.perf) * (tec.perfLim - computer.perf))
                             / tec.diagonal;
    }

    /* This is an ancillary method called by the adoptio method. It computes  *
     * the second element of the numerator in Equation 12                     */
    double distanceCovered() {
        return Math.sqrt(computer.cheap * computer.cheap + computer.perf * computer.perf) / tec.diagonal;
    }
    
    /* This method determines the outcomes of the innovation activity of the  *
     * firm, determining the level of perfromance and cheapness of the        *
     * computer produced by the firm and updating the level of experience     */
    void innovation() {
        
        double randomCheap = computerIndustry.muInn + rng.nextGaussian() * computerIndustry.sigmaInn;
        double randomPerf = computerIndustry.muInn + rng.nextGaussian() * computerIndustry.sigmaInn;
        
        /* Equation 1.a*/
        computer.perf += computerIndustry.betaPerf
                * Math.pow((tec.perfLim - computer.perf), computerIndustry.betaLim)
                * Math.pow(perfRdInput, computerIndustry.betaRes)
                * Math.pow(experience, computerIndustry.betaExp)
                * randomPerf;
        if (computer.perf > tec.perfLim) {
            computer.perf = tec.perfLim;
        }
        
        /* Equation 1.b*/
        computer.cheap += computerIndustry.betaCheap
                 * Math.pow((tec.cheapLim - computer.cheap), computerIndustry.betaLim)
                 * Math.pow(cheapRdInput, computerIndustry.betaRes)
                 * Math.pow(experience, computerIndustry.betaExp)
                 * randomCheap;
        if (computer.cheap > tec.cheapLim) {
            computer.cheap = tec.cheapLim;
        }
        
        experience++;
    }
    
    /* This method checks whether the computer produced by a firm that has    *
     * not entered the market so far satisfies the minimum performance and    *
     * cheapness thresholds of any user class.                                *
     * In case the conditions are satisfied, the firm enters that specific    *
     * user class                                                             */
    public void checkEntry(int TIME, UserClass USERCLASS) {
        
        if (!entered) {
            if ((computer.cheap > USERCLASS.lambdaCheap) && (computer.perf > USERCLASS.lambdaPerf)) {
                entered         = true;
                servedUserClass = USERCLASS;
            }
        }
    }
    
    /* This method updates the debt and budget accounts of the firm, and      *
     * checks whether it is still convenient to remain in the industry        */
    void accounting(int TIME) {
        
        if (debt > 0) {
            if ((profit > 0) && ((TIME - timeBirth > computerIndustry.projectTime))) {
                debt -= profit * computerIndustry.phiDebt;
                bud  -= profit * computerIndustry.phiDebt;
                if (debt < 0) {
                    bud  -= debt;
                    debt = 0;
                }
            }
            debt *= (1 + computerIndustry.r);
        }
        bud *= (1 + computerIndustry.r);
        double pastNormNw = normNw;
        normNw    = (bud - debt) / (initBud * Math.pow(1 + computerIndustry.r, TIME - timeBirth));
        double Y = normNw - pastNormNw;
        /* Equation 5                                                         */
        exitVar = (exitVar * (1 - computerIndustry.weightExit)) + (Y * computerIndustry.weightExit);
        if (entered && normNw < 0 && exitVar < computerIndustry.exitThreshold) {
            exitFirm();
        }
    }
    
    /* This method is activated when exit occurs: it switches the firm        *
     * controller of activitity to "FALSE" and resets the most relevant       *
     * variables                                                              */
    void exitFirm() {
        alive = false;
        debt  -= bud;
        bud   = 0;
        share = 0;
        mod   = 0;
        computer.cheap = 0;
        computer.perf  = 0;
    }

    /* This class contains the information about the technological trajectory *
     * of the firm that determines how R&D investment resources are allocated *
     * to cheapness and performance                                           */
    class Trajectory {

        // PARAMETERS
        double cheapMix;
        /* Fraction of resources allocated to cheapness research              */
        double perfMix;
        /* Fraction of resources allocated to performance research            */

        // CONSTRUCTOR
        Trajectory() {
            cheapMix = rng.nextDouble();
            perfMix = (1 - cheapMix);
        }
        
    }
    
    /* This class contains the information about the technological level of   *
     * the computer produced by the firm in the two attributes (cheapness and *
     * performance)                                                           */
    public class Product {

        // VARIABLES
        double cheap;
        /* Level of cheapness (Z-CH_f,t)                                      */
        double perf;
        /* Level of performance (Z-PE_f,t)                                    */
    }
    
}