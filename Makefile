modules := gameHub/ testmod/
out_dir := static/
src_dir := static_src/

files := $(foreach mod, $(modules), $(shell find $(addprefix $(mod), $(src_dir)) | grep .ts))
targets := $(subst .ts,.js, $(subst $(src_dir),$(out_dir), $(files)))
#targets = $(subst .ts,.js, $(files))

scripts: $(targets)
	

define ts_build_template =
$(1)$(out_dir)%.js: $(1)$(src_dir)%.ts
	tsc --outFile $$@ $$<
endef

$(foreach mod, $(modules), $(eval $(call ts_build_template, $(mod))))
