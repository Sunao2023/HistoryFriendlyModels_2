package Chapter3;

/*                                                                            *
 *  @author Gianluca Capone and Davide Sgobba                                 *
 *                                                                            */

/* This class contains all variables and parameters that identify the two     *
 * semiconductor technologies: transistors and microprocessors                */
class Technology {

    // PARAMETERS
    String label;
    /* Label of the technology                                                */
    double cheapLim;
    /* Cheapness technological frontier (LAMBDA-CH_k)                         */
    double perfLim;
    /* Performance technological frontier (LAMBDA-PE_k)                       */
    double diagonal;
    /* Diagonal: distance from the origin to the frontier (d_k)               */
    double minInitBud;
    /* Minimum value of initial firm budget (B-0_f,k)                         */
    double rangeInitBud;
    /* Range of value of initial firm budget (B-0_f,k)                        */
    int    numOfFirms;
    /* Number of potential firms (F_k)                                        */
    
    // CONSTRUCTOR
    Technology(String[] PARAMETERS ) {
        label       = PARAMETERS[1];
        cheapLim    = Double.parseDouble(PARAMETERS[2]);
        perfLim     = Double.parseDouble(PARAMETERS[3]);
        diagonal    = Math.sqrt(cheapLim * cheapLim + perfLim * perfLim);
        minInitBud  = Double.parseDouble(PARAMETERS[4]);
        rangeInitBud = Double.parseDouble(PARAMETERS[5]);
        numOfFirms  = Integer.parseInt(PARAMETERS[6]);
    }
    
}