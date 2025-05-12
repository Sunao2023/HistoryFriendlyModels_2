package Chapter4;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables that define firm heterogeneity in the    *
 * computer market (either Mainframes or PC market) and the methods that      *
 * operate over these variables                                               */
class ComputerFirm {
    
    // VARIABLES
    double componentRd;
    /* Amount of resources invested in component R&D (B-CO_f,t)               */
    double exitShare;
    /* Inverse exit propensity (E_f,t)                                        */
    int numOfDrawsCmp;
    /* Number of new potential component mods drawn by the firm (N-CO_f,t)    */
    int numOfDrawsSys;
    /* Number of new potential system mods drawn by the firm (N-SY_f,t)       */
    double probToInt;
    /* Integration probability (I_f,t)                                        */
    double propToInt;
    /* Integration propensity (i_f,t)                                         */
    double probToSpec;
    /* Specialization probability (SIGMA_f,t)                                 */
    double propToSpec;
    /* Specialization propensity (sigma_f,t)                                  */
    double price;
    /* Unit price charged by the computer firm (P_f,t))                       */
    double profit;
    /* Amount of profit earned by the firm (PI_f,t)                           */
    double qSold;
    /* Quantity of computers sold to customers (q_f,t)                        */
    double share;
    /* Market share of the firm (s_f,t)                                       */
    double systemRd;
    /* Amount of resources invested in system R&D (B-SY_f,t)                  */
    
    // PARAMETERS
    double spillover;
    /* Spillover of systemr R&D to component R&D in integrated firms (PSI-CO) */
                                                              
    //TECHNICAL VARIABLES & OBJECTS
    boolean alive;
    /* It takes value "TRUE" if the firm is alive and active on the market,   *
     * "FALSE" otherwise                                                      */
    boolean born;
    /* All firms start with "TRUE"- It takes the value "FALSE" as soon as     *
     * they select the first supplier                                         */
    int contractD;
    /* Duration of the current contract with the supplier                     */
    int contractTime;
    /* Starting period of the current contract with the supplier              */
    int id;
    /* Identifier of the firm                                                 */
    boolean integrated;
    /* It takes value "TRUE" if the firm is vertically integrated, "FALSE"    *
     * otherwise. All firms start with value "FALSE"                          */
    int intTime;
    /* Starting period of integration                                         */
    int supplierId;
    /* Identifier of current supplier                                         */
    int tId;
    /* Identifier of the Component technology. 0 = Transistor technology;     * 
     * 1 = Integrated Circuit technology; 2 = Microprocessor technology       */
    ComputerMarket ComputerMarket;
    /* Access to Computer Market                                              */
    EndProduct Computer;
    /* Computer product to be sold to customers                               */
    NotSoldComponent Component;
    /* Component element to be used in the computer                           */
    SystemElement SysteM;
    /* System element to be used in the computer                              */
    
    // CONSTRUCTOR
    ComputerFirm(int ID, boolean PC, double STARTSHARE, double SPILLOVER,
                 double MODSYS, ComputerMarket COMPUTERMARKET) {
        
        id             = ID;
        exitShare      = STARTSHARE;
        spillover      = SPILLOVER;
        alive          = true;
        born           = true;
        integrated     = false;
        tId            = 0;
        componentRd    = 0;
        profit         = 0;
        intTime        = 0;
        contractTime   = 0;
        contractD      = 0;
        supplierId     = -1;
        
        SysteM         = new SystemElement(MODSYS, this);
        Component      = new NotSoldComponent(this);
        Computer       = new EndProduct(this);
        ComputerMarket = COMPUTERMARKET;
    }

    /* This method determines the probability to integrate if the firm is a   *
     * specialized computer producer                                          */
    void calcProbToIntegrate(double QCO, int T) {
        
        if (QCO > 0) {
            /* Equation 16                                                    */
            propToInt = Math.pow(Math.min((T - ComputerMarket.entryTimeCmpTec[ComputerMarket.tIdCmp]) / ComputerMarket.chi0, 1), ComputerMarket.chi1)
                      * Math.pow((qSold / QCO), ComputerMarket.chi2);
            /* Equation 17                                                    */
            probToInt = (ComputerMarket.xiInt * propToInt)
                      / (1 + (ComputerMarket.xiInt * propToInt));
        } else {
            probToInt = 1;
        }
        
    }

    /* This method implements firm-level changes in case of integration       */
    void integrateVertically(ComponentFirm SUPPLIER, int TIME) {
        integrated            = true;
        Component.mod         = ComputerMarket.inheritance * SUPPLIER.Component.mod;
        tId                   = SUPPLIER.tId;
        intTime               = TIME;
        supplierId            = -1;
        contractTime          = 0;
        contractD             = 0;
    }
    
    /* This method determines the probability to specialize if the firm is an *
     * integrated computer producer                                           */
    void calcProbToSpecialize(double BESTCMPMOD) {
        
        /* Equation 18                                                        */
        propToSpec = (Math.max((BESTCMPMOD - Component.mod) / Component.mod, 0));
        /* Equation 19                                                        */
        probToSpec = (ComputerMarket.xiSpec * propToSpec)
                   / (1 + (ComputerMarket.xiSpec * propToSpec));
        
    }
    
    /* This method implements firm-level changes in case of specialization or *
     * when a new supplier is chosen                                          */
    void signContract(int SUPPLIERID, int TIME, int TID) {
        integrated            = false;
        supplierId            = SUPPLIERID;
        contractTime          = TIME;
        tId                   = TID;
        contractD             = ComputerMarket.minLengthContr
                              + ComputerMarket.rng.nextInt(ComputerMarket.rangeLengthContr);
        intTime               = 0;
    }

    /* This method computes the R&D expenditure and allocates the resources   *
     * to Component R&D and System R&D in the case of integrated firms        */
    void rdExpenditure() {
        
        systemRd = ComputerMarket.rdOnProf * profit;
        if (integrated) {
            /* Equation 12                                                    */
            systemRd -= ComputerMarket.rdOnProf * qSold * ComputerMarket.markup * Component.productionCost;
            if (systemRd > 0) {
                componentRd = (spillover * systemRd
                             + ComputerMarket.rdOnProf * qSold * ComputerMarket.markup * (Component.productionCost));
            } else {
                /* See footnote 15                                            */
                systemRd = 0;
                componentRd = ComputerMarket.rdOnProf * profit;
            }
        }
    }
    
    /* This method checks whether the integrated firm can switch to a new     *
     * component technology because of the high level of the public knowledge */
    void checkComponentTechnology(int TIME, double[] PK) {
        if (tId == 0) {
            if (TIME >= ComputerMarket.entryTimeCmpTec[1]) {
                double meanTemp = Math.log(PK[0]) * (1 - ComputerMarket.internalCum)
                                + Math.log(Component.mod) * ComputerMarket.internalCum;
                if (Math.log(PK[1]) > meanTemp) {
                    tId = 1;
                }
            }
        }
        if (tId == 1) {
            if (TIME >= ComputerMarket.entryTimeCmpTec[2]) {
                double meanTemp = Math.log(PK[1]) * (1 - ComputerMarket.internalCum)
                                + Math.log(Component.mod) * ComputerMarket.internalCum;
                if(Math.log(PK[2]) > meanTemp) {
                    tId = 2;
                }
            }
        }
    }
    
    /* This method determines the outcomes of the innovation activity of the  *
     * firm, determining the level of mod of the component produced by the    *
     * integrated computer firm                                               */
    void progressCmp() {
        
        double tempNumOfDraws = componentRd / ComputerMarket.drawCostCmp[tId];
        numOfDrawsCmp         = (int) Math.floor(tempNumOfDraws);
        double remain         = tempNumOfDraws - numOfDrawsCmp;
        double randomNumber   = ComputerMarket.rng.nextDouble();
        
        if (randomNumber <= remain) {
            numOfDrawsCmp++;
        }

        Component.calcMod();
    }
    
    /* This method determines the outcomes of the innovation activity of the  *
     * firm, determining the level of mod of the system produced by the       *
     * computer firm                                                          */
    void progressSys() {
        
        double tempNumOfDraws = systemRd / ComputerMarket.drawCostSys;
        numOfDrawsSys         = (int) Math.floor(tempNumOfDraws);
        double remain         = tempNumOfDraws - numOfDrawsSys;
        double randomNumber   = ComputerMarket.rng.nextDouble();
        
        if (randomNumber <= remain) {
            numOfDrawsSys++;
        }

        SysteM.calcMod();
    }
    
    /* This method computes the computer mod, and from it derives perfomance, *
     * cheapness, price, and production cost                                  */
    void computerModPriceCost() {

        Computer.calcMod();
        Computer.calcCheapPerf();
        if (Computer.mod > 0) {
            /* Equation 8                                                     */
            price =  ComputerMarket.nuComputer / (Computer.cheap);
        } else {
            price = 0;
        }
        Computer.calcCost();
    }
    
    /* This method computes the sales of the computer firm                    */
    void calcQuantitySold(int NUMOFEXTMKTS) {
        qSold = NUMOFEXTMKTS*Computer.modForCust;
    }
    
    /* This method updates the profits account of the firm                    */
    void accounting() {
        if (!integrated) {
            /* Equation 10                                                    */
            profit     = (Computer.productionCost * ComputerMarket.markup * qSold)
                       - (qSold * ComputerMarket.markup * Component.productionCost);
        }
        else {
            /* Equation 6                                                     */
            profit     = (Computer.productionCost * ComputerMarket.markup * qSold);
        }
    }
    
    /* This method computes the market share of the firm                      */
    void calcShare(double TOTSOLD) {
        if (TOTSOLD != 0) {
            share = qSold / TOTSOLD;
        } else {
            share = 0;
        }
    }
    
    /* This method checks whether the conditions to remain in the industry    *
     * still hold                                                             */
    boolean exitTheMarket() {
        
        boolean exit = false;
        exitShare = ((1 - ComputerMarket.weightExit) * exitShare)
                  + (ComputerMarket.weightExit * share);

        if (exitShare < ComputerMarket.exitThreshold) {
            exit = true;
        }
        return exit;
    }
    
    /* This method is activated when exit occurs: it switches the firm        *
     * controller of activitity to "FALSE" and resets the most relevant       *
     * variables at the firm and product level                                */
    void exitFirm() {
        alive        = false;
        supplierId   = -1;
        contractTime =  0;
        contractD    =  0;
        probToInt    = -1;
        propToInt    = -1;
        probToSpec   = -1;
        propToSpec   = -1;
        profit       =  0;
        systemRd     =  0;
        spillover    =  0;
        componentRd  =  0;
        price        =  0;
        qSold        =  0;
        share        =  0;
        Component.exitComponent();
        SysteM.exitSystem();
        Computer.exitComputer();
    }
    
}
