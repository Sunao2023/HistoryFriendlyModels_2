package Chapter4;

/*                                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

/* This class contains all elements to store and retrieve parameter values    */
class Parameter {
    
    // PARAMETERS ATTRIBUTES 
    private String name;
    /* Name of the parameter                                                  */
    private String value;
    /* Value of the parameter                                                 */
    private String variation;
    /* Range of variation for sensitivity analysis                            */
    private String conversionType;
    /* Type of parameter: Integer or Double                                   */
    private Boolean isUnderSA;
    /* Controller of sensitivity analysis                                     */

    // CONSTRUCTOR
    public Parameter() {
        name           = "";
        value          = "";
        variation      = "";
        conversionType = "";
        isUnderSA      = false;
    }

    /* The following are ancillary methods to set the values of the parameter *
     * attributes                                                             */
    void setName(String NAME) {
        name = NAME;
    }
    void setValue(String VALUE) {
        value = VALUE;
    }
    void setVariation(String VARIATION) {
        variation = VARIATION;
    }
    void setConversionType(String CONVERSIONTYPE) {
        conversionType = CONVERSIONTYPE;
    }
    void setIsUnderSA(Boolean ISUNDERSA) {
        isUnderSA = ISUNDERSA;
    }
    
    /* The following are ancillary methods to retrieve the values of the      *
     * parameter attributes                                                   */
    String getName() {
        return name;
    }
    String getValue() {
        return value;
    }
    String getVariation() {
        return variation;
    }
    Boolean getIsUnderSA() {
        return isUnderSA;
    }  
    String getConversionType() {
        return conversionType;
    }
}
