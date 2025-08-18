from enum import unique

from ......_base_enum import StrEnum


@unique
class BusinessSector(StrEnum):
    ACADEMIC_AND_EDUCATIONAL_SERVICES = "AcademicAndEducationalServices"
    APPLIED_RESOURCES = "AppliedResources"
    AUTOMOBILES_AND_AUTO_PARTS = "AutomobilesAndAutoParts"
    BANKING_AND_INVESTMENT_SERVICES = "BankingAndInvestmentServices"
    CHEMICALS = "Chemicals"
    COLLECTIVE_INVESTMENTS = "CollectiveInvestments"
    CONSUMER_GOODS_CONGLOMERATES = "ConsumerGoodsConglomerates"
    CYCLICAL_CONSUMER_PRODUCTS = "CyclicalConsumerProducts"
    CYCLICAL_CONSUMER_SERVICES = "CyclicalConsumerServices"
    ENERGY_FOSSIL_FUELS = "EnergyFossilFuels"
    FINANCIAL_TECHNOLOGY_AND_INFRASTRUCTURE = "FinancialTechnologyAndInfrastructure"
    FOOD_AND_BEVERAGES = "FoodAndBeverages"
    FOOD_AND_DRUG_RETAILING = "FoodAndDrugRetailing"
    GOVERNMENT_ACTIVITY = "GovernmentActivity"
    HEALTHCARE_SERVICES_AND_EQUIPMENT = "HealthcareServicesAndEquipment"
    INDUSTRIAL_AND_COMMERCIAL_SERVICES = "IndustrialAndCommercialServices"
    INDUSTRIAL_GOODS = "IndustrialGoods"
    INSTITUTIONS_ASSOCIATIONS_AND_ORGANIZATIONS = "InstitutionsAssociationsAndOrganizations"
    INSURANCE = "Insurance"
    INVESTMENT_HOLDING_COMPANIES = "InvestmentHoldingCompanies"
    MINERAL_RESOURCES = "MineralResources"
    PERSONAL_AND_HOUSEHOLD_PRODUCTS_AND_SERVICES = "PersonalAndHouseholdProductsAndServices"
    PHARMACEUTICALS_AND_MEDICAL_RESEARCH = "PharmaceuticalsAndMedicalResearch"
    REAL_ESTATE = "RealEstate"
    RENEWABLE_ENERGY = "RenewableEnergy"
    RETAILERS = "Retailers"
    SOFTWARE_AND_IT_SERVICES = "SoftwareAndITServices"
    TECHNOLOGY_EQUIPMENT = "TechnologyEquipment"
    TELECOMMUNICATIONS_SERVICES = "TelecommunicationsServices"
    TRANSPORTATION = "Transportation"
    URANIUM = "Uranium"
    UTILITIES = "Utilities"
