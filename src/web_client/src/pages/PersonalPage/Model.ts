// temp file
// contains help classes to store personal info

/**
 * Temp class.
 * We use it as storage of personal data.
 */
export class PersonalInfoModel {

    public constructor() {
        // tslint:disable-next-line:max-line-length
        this.personalNotes = "Возможно размещение короткого пояснительного текста о себе с указанием личных достижений и значимых наград Характер: спокойный, усидчивый, умение ставить цели и достигать их";

        this.hardSkills = [new HardSkillModel("целеустремленность", 90),
        new HardSkillModel("стрессоустойчивость", 79),
        new HardSkillModel("оперативность", 85),
        new HardSkillModel("готовность изучать новое", 60)];

        this.softSkills = [new SoftSkillModel("ответственность", 156),
        new SoftSkillModel("аккуратность", 85),
        new SoftSkillModel("организованость", 342)];
    }

    public personalNotes: string;
    public hardSkills: HardSkillModel[];
    public softSkills: SoftSkillModel[];
}

export class HardSkillModel {

    public constructor(name: string, value: number) {
        this.name = name;
        this.value = value;
    }

    public name: string;
    public value: number;
}

export class SoftSkillModel {
    public constructor(name: string, likesCount: number) {
        this.name = name;
        this.likesCount = likesCount;
    }

    public name: string;
    public likesCount: number;
}
