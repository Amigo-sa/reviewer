use reviewer

collections = db.getCollectionNames();
collections.forEach((coll) =>{
   db.getCollection(coll).drop();
});
/*
db.createCollection("service", {
  validator: {
    $jsonSchema:{
      additionalProperties : false,
      bsonType: "object",
      required: ["Version"],
      properties: {
        _id: {},
        Version: {
          bsonType: "string"
        }
      }
    }
  }
})
db.service.insertOne({Version: "0.2"})
/*
db.createCollection("person", {
  validator: {
    $jsonSchema: {
       additionalProperties: false,
       bsonType: "object",
       required: ["first_name", "surname"],
       properties: {
        _id: {},
        first_name: {
           bsonType: "string"
        },
        middle_name: {
           bsonType: "string"
        },
        surname: {
           bsonType: "string"
        },
        birth_date: {
            bsonType: "datetime"
        },
        phone_no:{
            bsonType: "string",
            pattern: "^[0-9]+$"
        }
      }
    }
  }
});

db.createCollection("soft_skill", {
  validator: {
    $jsonSchema: {
      additionalProperties: false,
      bsonType: "object",
        required: ["name", "level", "person_id"],
        properties: {
        _id: {},
        name: {
           bsonType: "string"
        },
        level: {
           bsonType: "double",
           minimum:  0.0,
           maximum:  100.0
        },
        personId: {
           bsonType: "objectId",
           description: "must refer to person document"
        }
      }
    }
  }
});

db.createCollection("hard_skill", {
  validator: {
    $jsonSchema: {
      additionalProperties: false,
      bsonType: "object",
        required: ["name", "level", "person_id"],
        properties: {
        _id: {},
        name: {
           bsonType: "string"
        },
        level: {
           bsonType: "double",
           minimum:  0.0,
           maximum:  100.0
        },
        personId: {
           bsonType: "objectId",
           description: "must refer to person document"
        }
      }
    }
  }
});

db.createCollection("organization", {
  validator: {
    $jsonSchema: {
      additionalProperties: false,
      bsonType: "object",
        required: ["name"],
        properties: {
        _id: {},
        name: {
           bsonType: "string"
        }
      }
    }
  }
});

db.createCollection("department", {
  validator: {
    $jsonSchema: {
      additionalProperties: false,
      bsonType: "object",
        required: ["name", "organization_id"],
        properties: {
        _id: {},
        name: {
           bsonType: "string"
        },
        organization_id: {
           bsonType: "objectId",
           description: "must refer to organization document"
        }
      }
    }
  }
});




/*



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
               bsonType: "string" //а можно привязать не к этому, а к какому-то глобальному идентификатору роли!
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

*/
