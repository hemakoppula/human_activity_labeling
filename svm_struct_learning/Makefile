# Makefile for SVM-struct API, 03.07.04

export

CC = gcc #gcc-4.4
LD = gcc #gcc-4.4
#CC = attolcc -mempro -perfpro -block -proc -- gcc
#LD = attolcc -mempro -perfpro -block -proc -- gcc
CFLAGS = -O3 -fomit-frame-pointer -ffast-math -Wall 
LDFLAGS = -O3 -lm -Wall
CFLAGS = -g -Wall
LDFLAGS = -g -lm
#CFLAGS = -pg -Wall
#LDFLAGS = -pg -lm -Wall 

OPTIMIZER := hideo
TARGETNAME := python
TRAIN_TARGET := svm_$(TARGETNAME)_learn
CLASS_TARGET := svm_$(TARGETNAME)_classify

DEFAULT_MODULE := multiclass
#DEFAULT_MODULE := svmstruct

PY_OBJS := $(patsubst %.c,%.o,$(wildcard pyobjs/*.c))

all: $(addsuffix $(OPTIMIZER),$(TRAIN_TARGET)_) $(CLASS_TARGET)

.PHONY: clean
clean: svm_light_clean svm_struct_clean
	rm -f *.o *.tcov *.d core gmon.out *.stackdump 
	rm -f $(PY_OBJS)
	rm -rf $(TRAIN_TARGET) $(CLASS_TARGET)

#-----------------------#
#----   Python dec  ----#
#-----------------------#

PYTHON := python
# Happily, thanks to the built-in distutils module, the Python
# interpreter is able to return many variables relating to its
# installation including where to look for the library, the library
# name, include files, and the special compiler directives that allow
# for dynamic loading of modules in programs that embed Python!
define PYTHON_COMMAND
-c "from distutils import sysconfig; print sysconfig.get_config_var('R')"
endef

PYTHON_LIB_DIR := $(shell $(PYTHON) $(subst R,LIBPL,$(PYTHON_COMMAND)))
PYTHON_LIB := $(basename $(patsubst lib%,%,$(shell $(PYTHON) $(subst R,LIBRARY,$(PYTHON_COMMAND)))))
PYTHON_INCLUDE := $(shell $(PYTHON) $(subst R,INCLUDEPY,$(PYTHON_COMMAND)))
PYTHON_SHARED := $(shell $(PYTHON) $(subst R,LINKFORSHARED,$(PYTHON_COMMAND)))
# Make it work on OS X with the Apple supplied python.
PYTHON_SHARED := $(PYTHON_SHARED:Python.framework/Versions/%/Python=-framework Python)
PYTHON_OTHER_LIBS := $(shell $(PYTHON) $(subst R,LIBS,$(PYTHON_COMMAND)))
PYTHON_LD_FLAGS := $(PYTHON_SHARED) -L$(PYTHON_LIB_DIR) -l$(PYTHON_LIB) $(PYTHON_OTHER_LIBS)
PYTHON_CC_FLAGS := -I$(PYTHON_INCLUDE)


#-----------------------#
#----   SVM-light   ----#
#-----------------------#
svm_light_hideo_noexe: 
	cd svm_light; make svm_learn_hideo_noexe

svm_light_loqo_noexe: 
	cd svm_light; make svm_learn_loqo_noexe

svm_light_clean: 
	cd svm_light; make clean

#----------------------#
#----  STRUCT SVM  ----#
#----------------------#

svm_struct_noexe:
	cd svm_struct; make svm_struct_noexe

svm_struct_clean:
	cd svm_struct; make clean

#-------------------------#
#----  SVM empty API  ----#
#-------------------------#

$(CLASS_TARGET): svm_light_hideo_noexe svm_struct_noexe svm_struct_api.o svm_struct/svm_struct_classify.o svm_struct/svm_struct_common.o svm_struct/svm_struct_main.o $(PY_OBJS)
	$(LD) $(LDFLAGS) svm_struct_api.o svm_struct/svm_struct_classify.o svm_light/svm_common.o svm_struct/svm_struct_common.o $(PY_OBJS) $(PYTHON_LD_FLAGS) $(LIBS) -lm -o $@

$(TRAIN_TARGET)_loqo: svm_light_loqo_noexe svm_struct_noexe svm_struct_api.o svm_struct/svm_struct_learn.o svm_struct/svm_struct_common.o svm_struct/svm_struct_main.o $(PY_OBJS)
	$(LD) $(LDFLAGS) svm_struct/svm_struct_learn.o svm_struct_api.o svm_light/svm_loqo.o svm_light/pr_loqo/pr_loqo.o svm_light/svm_learn.o svm_light/svm_common.o svm_struct/svm_struct_common.o svm_struct/svm_struct_main.o $(PY_OBJS) $(PYTHON_LD_FLAGS) $(LIBS) -lm -o $(TRAIN_TARGET)

$(TRAIN_TARGET)_hideo: $(TRAIN_TARGET)_% : svm_light_%_noexe svm_struct_noexe svm_struct_api.o  svm_struct/svm_struct_learn.o svm_struct/svm_struct_common.o svm_struct/svm_struct_main.o $(PY_OBJS)
	$(LD) $(LDFLAGS) svm_struct/svm_struct_learn.o svm_struct_api.o svm_light/svm_$*.o svm_light/svm_learn.o svm_light/svm_common.o svm_struct/svm_struct_common.o svm_struct/svm_struct_main.o $(PY_OBJS) $(PYTHON_LD_FLAGS) $(LIBS) -lm -o $(TRAIN_TARGET)

$(PY_OBJS): %.o : %.c %.h
	$(CC) -c $(CFLAGS) $(PYTHON_CC_FLAGS) $< -o $@

svm_struct_api.o: svm_struct_api.c svm_struct_api.h svm_struct_api_types.h svm_struct/svm_struct_common.h
	$(CC) -c $(CFLAGS) $(PYTHON_CC_FLAGS) -DDEFAULT_MODULE=$(DEFAULT_MODULE) $< -o $@ 
