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
         required: ["Name", "BirthDate"],
         properties: {
            _id: {},
            Name: {
               bsonType: "string"
            },
            BirthDate: {
                bsonType: "date"
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
               bsonType: "objectId"
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
               bsonType: "objectId"
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
               bsonType: "objectId"
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
               bsonType: "objectId"
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
               bsonType: "objectId"
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
               bsonType: "objectId"
            },
            DepartmentId: {
               bsonType: "objectId"
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
               bsonType: "objectId"
            },
            DepartmentId: {
               bsonType: "objectId"
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
                 bsonType: "objectId"
               }
            }
         }
      }
   }
});

db.createCollection("Reviews", {
   validator: {
      $jsonSchema: {
        additionalProperties: false,
        bsonType: "object",
        required: ["RoleId", "SubjectId", "Rate"],
        properties: {
            _id: {},
            RoleId: {
               bsonType: "objectId"
            },
            SubjectId: {
               bsonType: "objectId"
            },
            GroupId: {
               bsonType: "objectId"
            },
            Details: {
               bsonType: "string"
            },
            Rate: {
               bsonType: "double"
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
               bsonType: "objectId"
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
               bsonType: "objectId"
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
                     bsonType: "objectId"
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
