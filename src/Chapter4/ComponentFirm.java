package Chapter4;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all variables that define firm heterogeneity in the    *
 * component market and the methods that operate over these variables         */
class ComponentFirm {
    
    // VARIABLES
    double componentRd;
    /* Amount of resources invested in R&D (B-CO_f,t)                         */
    double countNoSales;
    /* Number of consecutive periods in which the firm does not sell to a     *
     * computer producer (T-E_f,t)                                            */
    int numOfDrawsCmp;
    /* Number of new potential component mods drawn by the firm (N-CO_f,t)    */
    double price;
    /* Unit price charged by the component firm (P_f,t))                      */
    double profit;
    /* Amount of profit earned by the firm (PI_f,t)                           */
    double share;
    /* Market share of the firm (s_f,t)                                       */
    double totalSold;
    /* Quantity of components sold  (q_f,h,t; q_f,t)                          */
    
    //TECHNICAL VARIABLES & OBJECTS
    boolean alive;
    /* It takes value "TRUE" if the firm is alive and active on the market,   *
     * "FALSE" otherwise                                                      */
    int[] buyerId;
    /* It identifies the computer firms that might buy from the component     *
     * firm. Each element in the vector represents a computer firm: the       *
     * element takes value "TRUE" if the computer firm buys from the          *
     * component firm, "FALSE" otherwise                                      */
    double externalSold;
    /* Quantity of components sold on the external markets                    */
    int howManyBuyersMF;
    /* Number of Mainframes firms that buy from the component firm            */
    int howManyBuyersPC;
    /* Number of PC firms that buy from the component firm                    */
    int id;
    /* Identifier of the firm                                                 */
    double qSold;
    /* Quantity of components sold to computer firms                          */
    int tId;
    /* Identifier of the Component technology. 0 = Transistor technology;     *
     * 1 = Integrated Circuit technology; 2 = Microprocessor technology       */
    SoldComponent Component;
    /* Component produced by the firm                                         */
    ComponentMarket CmpMarket;
    /* Access to component market                                             */
                  
    // CONSTRUCTOR
    ComponentFirm(int ID, int TID,double MOD, int NUMOFPOTENTIALBUYERS,
                  ComponentMarket CMPMARKET) {
        
        id           = ID;
        tId          = TID;
        alive        = true;
        componentRd  = 0;
        externalSold = 0;
        price        = 0;
        profit       = 0;
        qSold        = 0;
        share        = 0;
        totalSold    = 0;
        Component    = new SoldComponent(MOD, this);
        CmpMarket    = CMPMARKET;
        buyerId      = new int[NUMOFPOTENTIALBUYERS+1];
        
        for (int i = 0; i <= NUMOFPOTENTIALBUYERS; i++) {
            buyerId[i] = 0;
        }
    }

    /* This method computes the R&D expenditure                               */
    void rdExpenditure() {
        componentRd = CmpMarket.rdOnProf * profit;
    }
    
    /* This method determines the outcomes of the innovation activity of the  *
     * firm, determining the level of mod of the component produced by the    *
     * firm                                                                   */
    void progress() {
        
        /* Equation 13.b                                                      */
        double tempNumOfDraws = componentRd / CmpMarket.drawCost[tId];
        numOfDrawsCmp         = (int) Math.floor(tempNumOfDraws);
        double remain         = tempNumOfDraws - numOfDrawsCmp;
        double randomNumber   = CmpMarket.rng.nextDouble();
        
        if (randomNumber <= remain) {
            numOfDrawsCmp++;
        }

        Component.calcMod();
        /* Equation 7                                                         */
        price = Component.productionCost * (1 + CmpMarket.markup);
    }

    /* This method computes the quantity sold to the external markets         */
    void calcExternalSold(int NUMOFEXTMKTS) {
        /* Equation 5 adapted to components                                   */
        externalSold = NUMOFEXTMKTS*Component.mod;
    }
    
    /* This method updates the sales and profits accounts of the firm         */
    void accounting(ComputerMarket MF, ComputerMarket PC, boolean pcEntry) {
        
        qSold     = 0;
        totalSold = 0;
        howManyBuyersMF = 0;
        for (int f = 1; f <= MF.numOfFirms; f++) {
            if (buyerId[f] == 1) {
                qSold += MF.Firm[f].qSold * MF.numOfComp;
                howManyBuyersMF++;
            }
        }
        
        if (pcEntry) {
        
            howManyBuyersPC = 0;
            for (int f = MF.numOfFirms + 1; f <= MF.numOfFirms + PC.numOfFirms; f++) {
                if (buyerId[f] == 1) {
                    qSold += PC.Firm[f - MF.numOfFirms].qSold * PC.numOfComp;
                    howManyBuyersPC++;
                }
            }
        }
        totalSold = qSold + externalSold;
        /* Equation 6 adapted to components                                   */
        profit = totalSold * Component.productionCost * CmpMarket.markup;
    }
    
    /* Thie method computes the market share of the firm                      */
    void calcShare(double TOTSOLD) {
        if (TOTSOLD != 0) {
            share = totalSold / TOTSOLD;
        } else {
            share = 0;
        }
    }
    
    /* This method checks whether the conditions to remain in the industry    *
     * still hold                                                             */
    void checkExit() {
        
        double randomNumber = CmpMarket.rng.nextDouble();
        
        if (qSold == 0) {
            countNoSales++;
        } else {
            countNoSales = 0;
        }
        /* Equation 21                                                        */
        double exit = Math.pow((countNoSales / CmpMarket.exitThreshold), 2);
        if (exit > randomNumber) {
            exitFirm();
        }
        
    }
    
    /* This method is activated when exit occurs: it switches the firm        *
     * controller of activitity to "FALSE" and resets the most relevant       *
     * variables at the firm and product level                                */
    void exitFirm() {
        alive              = false;
        countNoSales       = 0;
        componentRd        = 0;
        externalSold       = 0;
        profit             = 0;
        price              = 0;
        qSold              = 0;
        share              = 0;
        totalSold          = 0;
        howManyBuyersMF    = 0;
        howManyBuyersPC    = 0;
        numOfDrawsCmp      = 0;
        
        for (int i = 0; i < buyerId.length; i++) {
            buyerId[i] = 0;
        }
        
        Component.exitComponent();
    }
    
    /* This method updates the list of buyers when a new contract is signed   */
    void signContract(int ID) {
        buyerId[ID] = 1;
    }
    
    /* This method updates the list of buyers when a contract expires         */
    void cancelContract(int ID) {
        buyerId[ID] = 0;
    }

}
