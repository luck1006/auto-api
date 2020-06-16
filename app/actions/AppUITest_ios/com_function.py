class Expected_result_check():


    def is_element_exist(self,driver, element):
        source = driver.page_source
        if element in source:
            return True
        else:
            return False
