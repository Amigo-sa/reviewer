import PersonDTO from "src/server-api/persons/Person";
import Person from "src/model/Person";

export default class DtoToBusinessConverter {

    public convertPerson(personDTO: PersonDTO): Person {
        const person = new Person();
        person.id = personDTO.id;
        person.firstName = personDTO.first_name;
        person.middleName = personDTO.middle_name;
        person.surname = personDTO.surname;
        person.birthDate = personDTO.birth_date;
        person.phone = personDTO.phone_no;
        person.organizationName = personDTO.organization_name;
        person.isHaveAvatar = personDTO.photo;
        person.departmentName = personDTO.department_name;
        person.specializationDisplayText = personDTO.specialization_display_text;
        person.notes = personDTO.notes;

        return person;
    }

}
