from lang_gen import LangGen

a = LangGen();
cont = LangGen.Content.COMMENT;
lang = LangGen.Language.FORTRAN;

a.addLine(cont, ["test"]);
