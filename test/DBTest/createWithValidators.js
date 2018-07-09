use reviewer

collections = db.getCollectionNames();
collections.forEach((coll) =>{
   db.getCollection(coll).drop();
});

db.createCollection("Persons", {
   validator: {
      $jsonSchema: {
         additionalProperties: false,
         bsonType: "object",
         required: ["FirstName", "BirthDate"],
         properties: {
            _id: {},
            FirstName: {
               bsonType: "string"
            },
            MiddleName: {
               bsonType: "string"
            },
            Surname: {
               bsonType: "string"
            },
            BirthDate: {
                bsonType: "date"
            },
            PhoneNo:{
                bsonType: "string",
                pattern: "^[0-9]+$"
            }
         }
      }
   }
});

db.createCollection("Skills", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "Level", "PersonId"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            Level: {
               bsonType: "double",
               minimum:  0.0,
               maximum:  120.0
            },
            PersonId: {
               bsonType: "objectId",
               description: "must refer to Person document"
            }
         }
      }
   }
});

db.createCollection("Features", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "Rate", "PersonId"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            Rate: {
                bsonType: "double",
                minimum:  0.0,
                maximum:  10.0
            },
            PersonId: {
               bsonType: "objectId",
               description: "must refer to Person document"
            }
         }
      }
   }
});

db.createCollection("Organizations", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            }
         }
      }
   }
});

db.createCollection("Universities", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "OrganizationId"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            OrganizationId: {
               bsonType: "objectId",
               description: "must refer to Organizaion document"
            }
         }
      }
   }
});

db.createCollection("Schools", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "OrganizationId"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            OrganizationId: {
               bsonType: "objectId",
               description: "must refer to Organizaion document"
            }
         }
      }
   }
});

db.createCollection("Departments", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "UniversityId"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            UniversityId: {
               bsonType: "objectId",
               description: "must refer to University document"
            }
         }
      }
   }
});

db.createCollection("StudentRoles", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["PersonId", "DepartmentId"],
        properties: {
            _id: {},
            PersonId: {
               bsonType: "objectId",
               description: "must refer to Person document"
            },
            DepartmentId: {
               bsonType: "objectId",
               description: "must refer to Department document"
            },
            Specialization: {
               bsonType: "string"
            }
         }
      }
   }
});

db.createCollection("TutorRoles", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["PersonId", "DepartmentId"],
        properties: {
            _id: {},
            PersonId: {
               bsonType: "objectId",
               description: "must refer to Person document"
            },
            DepartmentId: {
               bsonType: "objectId",
               description: "must refer to Department document"
            },
            Disciplines: {
               bsonType: "array",
               items: {
                 bsonType: "string"
               }
            }
         }
      }
   }
});

db.createCollection("Groups", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "RoleList"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            RoleList: {
               bsonType: "array",
               items: {
                 bsonType: "string",
                 description: "list of roles available for group"
               }
            }
         }
      }
   }
});

db.createCollection("GroupRoles", {
   validator: {
      $jsonSchema: {
         additionalProperties: false,
         bsonType: "object",
         required: ["RoleName", "GroupId", "PersonId"],
         properties: {
            _id: {},
            RoleName: {
               bsonType: "string"
            },
            GroupId: {
               bsonType: "objectId",
               description: "must refer to Group document"
            },
            PersonId: {
               bsonType: "objectId",
               description: "must refer to Person document"
            },
         }
      }
   }
});


db.createCollection("Reviews", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["PersonId", "SubjectId", "Rate"],
        properties: {
            _id: {},
            PersonId: {
               bsonType: "objectId",
               description: "must refer to Person document"
            },
            SubjectId: {
               bsonType: "objectId",
               description: "must refer to TutorRole, StudentRole, Group, Department, University, School, Skill or Feature document"
            },
            GroupId: {
               bsonType: "objectId",
               description: "must refer to Group document"
            },
            Details: {
               bsonType: "string"
            },
            Rate: {
               bsonType: "double",
               minimum: 0.0,
               maximum: 10.0
            }
         }
      }
   }
});

db.createCollection("Surveys", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "GroupId"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            GroupId: {
               bsonType: "objectId",
               description: "must refer to Group document"
            },
            Description: {
               bsonType: "string"
            },
            Results: {
               bsonType: "array",
               items: {
                 bsonType: "object",
                 additionalProperties: false,
                 required:["Parameter"],
                 properties:{
                   Parameter:{
                     bsonType: "string"
                   },
                   Quantity:{
                     bsonType: "double",
                   }
                 }
               }
            }
         }
      }
   }
});

db.createCollection("Tests", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["Name", "GroupId"],
        properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            GroupId: {
               bsonType: "objectId",
               description: "must refer to Group document"
            },
            Description: {
               bsonType: "string"
            },
            Results: {
               bsonType: "array",
               items: {
                 bsonType: "object",
                 additionalProperties: false,
                 required:["ParticipantId"],
                 properties:{
                   ParticipantId:{
                     bsonType: "objectId",
                     description: "must refer to StudentRole document"
                   },
                   Result:{
                     bsonType: "double",
                     minimum: 0.0,
                     maximum: 100.0
                   }
                 }
               }
            }
         }
      }
   }
});
